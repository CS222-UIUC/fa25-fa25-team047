import os
import json
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from flask directory
flask_dir = Path(__file__).parent
load_dotenv(dotenv_path=flask_dir / '.env')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("WARNING: OPENAI_API_KEY not found in environment variables")
openai_client = OpenAI(api_key=api_key) if api_key else None

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.post('/auth/login')
def login():
    payload = request.get_json(silent=True) or {}
    email = payload.get('email', '').strip()
    password = payload.get('password', '')

    if not email or '@' not in email:
        return (
            jsonify({'error': 'A valid email address is required.'}),
            400,
        )

    if not password or len(password) < 8:
        return (
            jsonify({'error': 'Password must be at least 8 characters long.'}),
            400,
        )

    token = f"dummy-session-{uuid4().hex}"
    return jsonify({'token': token, 'email': email})

@app.post('/api/chat')
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get('message', '').strip()
    conversation_history = payload.get('history', [])

    if not message:
        return jsonify({'error': 'Message is required.'}), 400

    # Detect a request for a coding challenge
    normalized = message.lower()
    wants_challenge, difficulty, topic = detect_challenge_request(normalized)

    if wants_challenge:
        if not openai_client:
            fallback = get_fallback_challenge(difficulty=difficulty, topic=topic)
            return jsonify({
                'message': "Using a fallback challenge because no OpenAI API key is configured.",
                'challenge': fallback,
                'error': 'OpenAI client not initialized. Please check API key.',
            }), 200
        try:
            challenge = generate_coding_challenge(
                user_prompt=message,
                difficulty=difficulty,
                topic=topic,
            )
            if challenge is None:
                raise RuntimeError("challenge generation returned None")

            assistant_message = (
                f"Here is a {difficulty} coding problem"
                f"{f' about {topic}' if topic else ''}: {challenge.get('title', 'Unknown Title')}."
            )
            return jsonify({
                'message': assistant_message,
                'challenge': challenge
            })
        except Exception as e:
            print(f"Error generating coding challenge: {str(e)}")
            fallback = get_fallback_challenge(difficulty=difficulty, topic=topic)
            print("Using fallback challenge.")
            return jsonify({
                'message': f"OpenAI generation failed ({str(e)}). Using a fallback challenge instead.",
                'challenge': fallback,
                'error': str(e),
            }), 200

    try:
        # Prepare messages for OpenAI API
        messages = []
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })

        # Call OpenAI API
        # TODO: Replace with actual OpenAI call when quota is available
        # response = openai_client.chat.completions.create(
        #     model="gpt-4",
        #     messages=messages,
        #     temperature=0.7,
        #     max_tokens=1000
        # )
        # assistant_message = response.choices[0].message.content

        # Temporary mock response for testing
        assistant_message = f"This is a test response to your message: '{message}'"

        return jsonify({
            'message': assistant_message
        })
    
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        if not openai_client:
            # When running without an API key, fall back to a mock response so the UI remains usable.
            return jsonify({
                'message': f"(mock) This is a test response to your message: '{message}'",
                'warning': 'OpenAI client not initialized. Please check API key.',
            }), 200
        return jsonify({'error': 'Failed to get response from AI.'}), 500

def detect_challenge_request(normalized: str):
    """
    Heuristically decide if the user wants a generated coding problem.
    Returns (is_challenge, difficulty, topic)
    """
    verbs = ["give", "generate", "create", "make", "build", "random", "practice", "need", "want"]
    has_generation_intent = any(v in normalized for v in verbs)
    mentions_problem = "leetcode" in normalized or "coding challenge" in normalized or ("problem" in normalized and has_generation_intent) or ("challenge" in normalized and has_generation_intent)

    difficulty = "Hard"
    if "easy" in normalized:
        difficulty = "Easy"
    elif "medium" in normalized:
        difficulty = "Medium"
    elif "hard" in normalized:
        difficulty = "Hard"

    topic = None
    if "binary tree" in normalized or "tree" in normalized:
        topic = "Binary Trees"
    if "kahn" in normalized or "topological" in normalized:
        topic = "Topological Sort (Kahn's algorithm)"
    if "consecutive" in normalized:
        topic = "Consecutive integers sequences"
    if "graph" in normalized and topic is None:
        topic = "Graphs"

    wants_challenge = mentions_problem or topic is not None
    return wants_challenge, difficulty, topic

def generate_coding_challenge(user_prompt: str, difficulty: str, topic: str | None = None):
    """
    Ask OpenAI for a structured LeetCode-style coding challenge with
    3 visible tests and 15 hidden tests. Returns a JSON-serializable dict.
    """
    system_prompt = """You are a coding interview problem generator.
Return ONLY strict JSON (no code fences, no explanations) with the shape:
{
  "title": "Concise problem title",
  "difficulty": "One of: Easy, Medium, Hard",
  "description": "Clear problem statement with constraints and at least one example. Keep it under 180 words.",
  "function_signature": "def solve(input):\\n    # describe parameters\\n    pass",
  "starter_code": "def solve(input):\\n    # input: describe shape\\n    # TODO: implement\\n    return None\\n",
  "visible_tests": [
    {"description": "case 1", "input_json": "...", "expected_json": "..."},
    {"description": "case 2", "input_json": "...", "expected_json": "..."},
    {"description": "case 3", "input_json": "...", "expected_json": "..."}
  ],
  "hidden_tests": [
    {"description": "hidden 1", "input_json": "...", "expected_json": "..."},
    ... 15 total hidden tests ...
  ]
}

Rules:
- input_json and expected_json must be valid JSON strings (no comments) that can be parsed directly with JSON.parse.
- Design the problem so a single function solve(input) is enough.
- Hidden tests should vary sizes and edge cases.
- Use primitives, arrays, or objects; avoid language-specific types.
- Do not wrap the response in ```; respond with JSON only.
- Match the requested difficulty and, if provided, the requested topic/algorithm."""

    user_instruction = f"User request: {user_prompt}. Generate a LeetCode-style {difficulty.upper()} problem."
    if topic:
        user_instruction += f" Focus on the topic: {topic}."

    last_error: Exception | None = None
    last_content: str | None = None
    for attempt in range(3):  # retry on API or parse errors
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_instruction}
                ],
                temperature=0.4,
                max_tokens=900,
                response_format={"type": "json_object"},
            )
            content = completion.choices[0].message.content
            last_content = content
            try:
                return parse_challenge_response(content)
            except Exception as parse_error:
                last_error = parse_error
                print(f"OpenAI parse attempt {attempt + 1} failed: {parse_error}")
                continue
        except Exception as api_error:
            last_error = api_error
            print(f"OpenAI API attempt {attempt + 1} failed: {api_error}")
            continue

    # If we got here, all attempts failed.
    summary = f"{last_error}"
    if last_content:
        snippet = last_content[:400].replace("\n", " ")
        summary += f" | last_content_snippet: {snippet}"
    raise RuntimeError(f"Challenge generation failed after retries: {summary}")

def get_fallback_challenge(difficulty: str = "Hard", topic: str | None = None):
    """Static challenges used if OpenAI fails, so UI stays usable."""
    # Library of simple fallbacks keyed by topic/difficulty.
    fallbacks = {
        ("Easy", "Binary Trees"): {
            "title": "Maximum Depth of Binary Tree",
            "difficulty": "Easy",
            "description": "Given the root of a binary tree, return its maximum depth.",
            "function_signature": "def solve(root):\n    # root is serialized as [val, left, right] or None\n    pass",
            "starter_code": (
                "def solve(root):\n"
                "    \"\"\"Return maximum depth of binary tree serialized as [val, left, right].\"\"\"\n"
                "    def dfs(node):\n"
                "        if node is None:\n"
                "            return 0\n"
                "        _, left, right = node\n"
                "        return 1 + max(dfs(left), dfs(right))\n"
                "\n"
                "    return dfs(root)\n"
            ),
            "visible_tests": [
                {"description": "Single node", "input_json": "[1,null,null]", "expected_json": "1"},
                {"description": "Balanced small", "input_json": "[1,[2,null,null],[3,null,null]]", "expected_json": "2"},
                {"description": "Skewed", "input_json": "[1,[2,[3,null,null],null],null]", "expected_json": "3"},
            ],
            "hidden_tests": [
                {"description": "Empty", "input_json": "null", "expected_json": "0"},
                {"description": "Left heavy", "input_json": "[1,[2,[3,[4,null,null],null],null],null]", "expected_json": "4"},
                {"description": "Right heavy", "input_json": "[1,null,[2,null,[3,null,[4,null,null]]]]", "expected_json": "4"},
                {"description": "Full depth 3", "input_json": "[1,[2,[4,null,null],[5,null,null]],[3,[6,null,null],[7,null,null]]]", "expected_json": "3"},
                {"description": "Mixed", "input_json": "[5,[1,null,[7,null,null]],[3,[2,null,null],null]]", "expected_json": "3"},
                {"description": "Depth 5", "input_json": "[0,[1,[2,[3,[4,null,null],null],null],null],null]", "expected_json": "5"},
                {"description": "Depth 2", "input_json": "[0,[1,null,null],null]", "expected_json": "2"},
                {"description": "Depth 1", "input_json": "[10,null,null]", "expected_json": "1"},
                {"description": "Depth 4", "input_json": "[1,[2,[3,[4,null,null],null],null],null]", "expected_json": "4"},
                {"description": "Depth 3 alt", "input_json": "[1,[2,null,[4,null,null]],[3,null,null]]", "expected_json": "3"},
                {"description": "Depth 3 alt2", "input_json": "[1,[2,[4,null,null],null],[3,null,null]]", "expected_json": "3"},
                {"description": "Depth 3 alt3", "input_json": "[1,[2,[4,null,null],null],[3,[5,null,null],null]]", "expected_json": "3"},
                {"description": "Depth 4 zig", "input_json": "[1,[2,null,[3,null,[4,null,null]]],null]", "expected_json": "4"},
                {"description": "Depth 4 zag", "input_json": "[1,null,[2,null,[3,null,[4,null,null]]]]", "expected_json": "4"},
                {"description": "Depth 2 alt", "input_json": "[1,[2,null,null],[3,null,null]]", "expected_json": "2"},
            ],
        },
        ("Medium", "Consecutive integers sequences"): {
            "title": "Longest Consecutive Sequence",
            "difficulty": "Medium",
            "description": "Given an unsorted array of integers, return the length of the longest consecutive elements sequence.",
            "function_signature": "def solve(nums):\n    # nums: List[int]\n    pass",
            "starter_code": (
                "def solve(nums):\n"
                "    \"\"\"Return length of longest consecutive integer sequence.\"\"\"\n"
                "    num_set = set(nums)\n"
                "    best = 0\n"
                "    for n in num_set:\n"
                "        if n - 1 not in num_set:\n"
                "            length = 1\n"
                "            cur = n + 1\n"
                "            while cur in num_set:\n"
                "                length += 1\n"
                "                cur += 1\n"
                "            best = max(best, length)\n"
                "    return best\n"
            ),
            "visible_tests": [
                {"description": "Simple", "input_json": "[100,4,200,1,3,2]", "expected_json": "4"},
                {"description": "Single element", "input_json": "[0]", "expected_json": "1"},
                {"description": "Duplicates", "input_json": "[1,2,0,1]", "expected_json": "3"},
            ],
            "hidden_tests": [
                {"description": "Already sorted", "input_json": "[1,2,3,4,5]", "expected_json": "5"},
                {"description": "Negative numbers", "input_json": "[-2,-3,-1,-4]", "expected_json": "4"},
                {"description": "Gaps", "input_json": "[10,5,12,3,55,30,4,11,2]", "expected_json": "4"},
                {"description": "Large gap", "input_json": "[0,1000000]", "expected_json": "1"},
                {"description": "Mixed", "input_json": "[9,1,4,7,3,-1,0,5,8,-1,6]", "expected_json": "7"},
                {"description": "Repeats", "input_json": "[1,2,2,2,3]", "expected_json": "3"},
                {"description": "Two sequences", "input_json": "[10,11,12,1,2,3]", "expected_json": "3"},
                {"description": "Spread out", "input_json": "[100,101,102,50,51]", "expected_json": "3"},
                {"description": "Negative spread", "input_json": "[-5,-4,-3,-10]", "expected_json": "3"},
                {"description": "Mixed small", "input_json": "[5,2,99,3,4,1,100]", "expected_json": "5"},
                {"description": "Single", "input_json": "[42]", "expected_json": "1"},
                {"description": "Empty", "input_json": "[]", "expected_json": "0"},
                {"description": "Overlap", "input_json": "[0,0,1,1,2,2]", "expected_json": "3"},
                {"description": "Descending", "input_json": "[5,4,3,2,1]", "expected_json": "5"},
                {"description": "Non-consecutive", "input_json": "[10,30,20]", "expected_json": "1"},
            ],
        },
        ("Hard", "Topological Sort (Kahn's algorithm)"): {
            "title": "Unique Topological Ordering",
            "difficulty": "Hard",
            "description": (
                "Given n labeled nodes 0..n-1 and a list of directed edges, return the unique topological ordering "
                "if it exists, otherwise return an empty array. Use Kahn's algorithm. If multiple orders exist, return []."
            ),
            "function_signature": "def solve(input):\n    # input: {\"n\": int, \"edges\": List[List[int]]}\n    pass",
            "starter_code": (
                "from collections import deque\n"
                "\n"
                "def solve(input):\n"
                "    \"\"\"Return unique topo order using Kahn's algorithm, else [].\"\"\"\n"
                "    n = input[\"n\"]\n"
                "    edges = input[\"edges\"]\n"
                "    indeg = [0] * n\n"
                "    graph = [[] for _ in range(n)]\n"
                "    for u, v in edges:\n"
                "        graph[u].append(v)\n"
                "        indeg[v] += 1\n"
                "\n"
                "    q = deque([i for i, d in enumerate(indeg) if d == 0])\n"
                "    order = []\n"
                "    while q:\n"
                "        if len(q) > 1:\n"
                "            return []  # not unique\n"
                "        u = q.popleft()\n"
                "        order.append(u)\n"
                "        for v in graph[u]:\n"
                "            indeg[v] -= 1\n"
                "            if indeg[v] == 0:\n"
                "                q.append(v)\n"
                "\n"
                "    return order if len(order) == n else []\n"
            ),
            "visible_tests": [
                {"description": "Simple chain", "input_json": "{\"n\":3,\"edges\":[[0,1],[1,2]]}", "expected_json": "[0,1,2]"},
                {"description": "Branch but unique", "input_json": "{\"n\":4,\"edges\":[[0,1],[0,2],[2,3],[1,3]]}", "expected_json": "[0,1,2,3]"},
                {"description": "Cycle", "input_json": "{\"n\":2,\"edges\":[[0,1],[1,0]]}", "expected_json": "[]"},
            ],
            "hidden_tests": [
                {"description": "Multiple zeros -> not unique", "input_json": "{\"n\":3,\"edges\":[]}", "expected_json": "[]"},
                {"description": "Diamond not unique", "input_json": "{\"n\":4,\"edges\":[[0,1],[0,2],[1,3],[2,3]]}", "expected_json": "[]"},
                {"description": "Long chain", "input_json": "{\"n\":5,\"edges\":[[0,1],[1,2],[2,3],[3,4]]}", "expected_json": "[0,1,2,3,4]"},
                {"description": "Single node", "input_json": "{\"n\":1,\"edges\":[]}", "expected_json": "[0]"},
                {"description": "Two nodes disconnected", "input_json": "{\"n\":2,\"edges\":[]}", "expected_json": "[]"},
                {"description": "Tree like unique", "input_json": "{\"n\":5,\"edges\":[[0,1],[1,2],[2,3],[3,4],[0,2],[1,3],[2,4]]}", "expected_json": "[0,1,2,3,4]"},
                {"description": "Cycle large", "input_json": "{\"n\":4,\"edges\":[[0,1],[1,2],[2,3],[3,1]]}", "expected_json": "[]"},
                {"description": "Unique small", "input_json": "{\"n\":3,\"edges\":[[0,1],[0,2],[1,2]]}", "expected_json": "[0,1,2]"},
                {"description": "Not unique small", "input_json": "{\"n\":3,\"edges\":[[0,2]]}", "expected_json": "[]"},
                {"description": "Disconnected unique impossible", "input_json": "{\"n\":4,\"edges\":[[1,2],[2,3]]}", "expected_json": "[]"},
                {"description": "Cycle self", "input_json": "{\"n\":2,\"edges\":[[0,0]]}", "expected_json": "[]"},
                {"description": "Another unique", "input_json": "{\"n\":4,\"edges\":[[0,1],[1,2],[2,3]]}", "expected_json": "[0,1,2,3]"},
                {"description": "Another not unique", "input_json": "{\"n\":4,\"edges\":[[0,2],[1,2]]}", "expected_json": "[]"},
                {"description": "Multiple sources unique", "input_json": "{\"n\":3,\"edges\":[[0,1],[0,2],[1,2]]}", "expected_json": "[0,1,2]"},
                {"description": "Multiple sinks", "input_json": "{\"n\":3,\"edges\":[[0,1]]}", "expected_json": "[]"},
            ],
        },
        ("Hard", "Binary Trees"): {
            "title": "Serialize and Deserialize Binary Tree",
            "difficulty": "Hard",
            "description": (
                "Design an algorithm to serialize and deserialize a binary tree. Use pre-order with null markers."
            ),
            "function_signature": "def solve(input):\n    # input: [\"serialize\"|\"deserialize\", payload]\n    pass",
            "starter_code": (
                "def serialize(root):\n"
                "    if root is None:\n"
                "        return [None]\n"
                "    val, left, right = root\n"
                "    return [val] + serialize(left) + serialize(right)\n"
                "\n"
                "def deserialize(values):\n"
                "    it = iter(values)\n"
                "    def build():\n"
                "        try:\n"
                "            val = next(it)\n"
                "        except StopIteration:\n"
                "            return None\n"
                "        if val is None:\n"
                "            return None\n"
                "        left = build()\n"
                "        right = build()\n"
                "        return [val, left, right]\n"
                "    return build()\n"
                "\n"
                "def solve(input):\n"
                "    op, payload = input\n"
                "    if op == \"serialize\":\n"
                "        return serialize(payload)\n"
                "    if op == \"deserialize\":\n"
                "        return deserialize(payload)\n"
                "    return None\n"
            ),
            "visible_tests": [
                {"description": "Serialize simple", "input_json": "[\"serialize\",[1,[2,null,null],[3,null,null]]]", "expected_json": "[1,2,null,null,3,null,null]"},
                {"description": "Deserialize simple", "input_json": "[\"deserialize\",[1,2,null,null,3,null,null]]", "expected_json": "[1,[2,null,null],[3,null,null]]"},
                {"description": "Serialize null", "input_json": "[\"serialize\",null]", "expected_json": "[null]"},
            ],
            "hidden_tests": [
                {"description": "Deserialize null", "input_json": "[\"deserialize\",[null]]", "expected_json": "null"},
                {"description": "Serialize skewed", "input_json": "[\"serialize\",[1,[2,[3,null,null],null],null]]", "expected_json": "[1,2,3,null,null,null,null]"},
                {"description": "Deserialize skewed", "input_json": "[\"deserialize\",[1,2,3,null,null,null,null]]", "expected_json": "[1,[2,[3,null,null],null],null]"},
                {"description": "Full tree", "input_json": "[\"serialize\",[1,[2,[4,null,null],[5,null,null]],[3,[6,null,null],[7,null,null]]]]", "expected_json": "[1,2,4,null,null,5,null,null,3,6,null,null,7,null,null]"},
                {"description": "Deserialize full", "input_json": "[\"deserialize\",[1,2,4,null,null,5,null,null,3,6,null,null,7,null,null]]", "expected_json": "[1,[2,[4,null,null],[5,null,null]],[3,[6,null,null],[7,null,null]]]"},
                {"description": "Empty markers", "input_json": "[\"deserialize\",[]]", "expected_json": "null"},
                {"description": "Single node", "input_json": "[\"serialize\",[5,null,null]]", "expected_json": "[5,null,null]"},
                {"description": "Single deserialize", "input_json": "[\"deserialize\",[5,null,null]]", "expected_json": "[5,null,null]"},
                {"description": "Mixed", "input_json": "[\"deserialize\",[1,null,2,null,3,null,null]]", "expected_json": "[1,null,[2,null,[3,null,null]]]"},
                {"description": "Another mixed", "input_json": "[\"serialize\",[1,null,[2,null,[3,null,null]]]]", "expected_json": "[1,null,2,null,3,null,null]"},
                {"description": "Left heavy", "input_json": "[\"serialize\",[1,[2,[3,[4,null,null],null],null],null]]", "expected_json": "[1,2,3,4,null,null,null,null,null]"},
                {"description": "Right heavy", "input_json": "[\"serialize\",[1,null,[2,null,[3,null,[4,null,null]]]]]", "expected_json": "[1,null,2,null,3,null,4,null,null]"},
                {"description": "Null children", "input_json": "[\"serialize\",[1,null,null]]", "expected_json": "[1,null,null]"},
                {"description": "Deserialize tricky", "input_json": "[\"deserialize\",[1,null,2,3,null,null,null]]", "expected_json": "[1,null,[2,[3,null,null],null]]"},
                {"description": "Deserialize tricky 2", "input_json": "[\"deserialize\",[1,2,null,3,null,null,null]]", "expected_json": "[1,[2,[3,null,null],null],null]"},
            ],
        },
        ("Hard", None): {
            "title": "Longest Balanced Subarray of 0s and 1s",
            "difficulty": "Hard",
            "description": (
                "Given a binary array nums (only 0 and 1), return the length of the longest "
                "contiguous subarray that contains an equal number of 0s and 1s. "
                "If no such subarray exists, return 0. Constraints: 1 <= len(nums) <= 2e5."
            ),
            "function_signature": "def solve(nums):\n    # nums: List[int] of 0s and 1s\n    pass",
            "starter_code": (
                "def solve(nums):\n"
                "    \"\"\"Return length of longest subarray with equal 0s and 1s.\"\"\"\n"
                "    first_index = {0: -1}\n"
                "    diff = 0\n"
                "    best = 0\n"
                "    for i, val in enumerate(nums):\n"
                "        diff += 1 if val == 1 else -1\n"
                "        if diff in first_index:\n"
                "            best = max(best, i - first_index[diff])\n"
                "        else:\n"
                "            first_index[diff] = i\n"
                "    return best\n"
            ),
            "visible_tests": [
                {"description": "Simple balanced", "input_json": "[0,1]", "expected_json": "2"},
                {"description": "Unbalanced overall but has window", "input_json": "[0,0,1,0,1,1,0]", "expected_json": "6"},
                {"description": "No balanced subarray", "input_json": "[0,0,0]", "expected_json": "0"}
            ],
            "hidden_tests": [
                {"description": "all ones", "input_json": "[1,1,1,1]", "expected_json": "0"},
                {"description": "alternating", "input_json": "[0,1,0,1,0,1,0,1]", "expected_json": "8"},
                {"description": "prefix long", "input_json": "[1,1,0,0,0,1,1,0,0,1,1,0]", "expected_json": "12"},
                {"description": "single element", "input_json": "[1]", "expected_json": "0"},
                {"description": "two elements", "input_json": "[1,0]", "expected_json": "2"},
                {"description": "skewed then balance", "input_json": "[1,1,1,0,0,0,1,0,0,1,1,0,1,0]", "expected_json": "14"},
                {"description": "small window", "input_json": "[1,1,0]", "expected_json": "2"},
                {"description": "late balance", "input_json": "[1,1,1,1,0,0,0,0]", "expected_json": "8"},
                {"description": "balance in middle", "input_json": "[0,0,1,1,0,1,0,1,1,0,0,1]", "expected_json": "12"},
                {"description": "multiple options", "input_json": "[0,1,1,0,1,0,0,1]", "expected_json": "8"},
                {"description": "long ones then zeros", "input_json": "[1,1,1,1,1,0,0,0,0,0]", "expected_json": "10"},
                {"description": "random mix", "input_json": "[0,1,0,0,1,1,1,0,0,1,0,1,0,0]", "expected_json": "14"},
                {"description": "edge even", "input_json": "[0,0,1,1]", "expected_json": "4"},
                {"description": "edge odd", "input_json": "[0,1,1,1,0]", "expected_json": "2"},
                {"description": "large imbalance", "input_json": "[1,1,1,1,1,1,1,0,0,0,0,0,0]", "expected_json": "12"},
            ],
        },
    }

    key = (difficulty, topic) if topic else None
    if key and key in fallbacks:
        return fallbacks[key]
    # Try difficulty-only
    key = (difficulty, None)
    if key in fallbacks:
        return fallbacks[key]
    # Final fallback
    return fallbacks[("Hard", None)]


def parse_challenge_response(raw: str):
    """
    Try a few lenient parses to handle occasional code fences or trailing text
    from the model before falling back.
    """
    candidates = []
    cleaned = raw.strip()
    candidates.append(cleaned)
    # Strip code fences if present.
    if cleaned.startswith("```"):
        candidates.append(re.sub(r"^```(?:json)?", "", cleaned).rstrip("`").strip())
        for part in cleaned.split("```"):
            if "{" in part:
                candidates.append(part.strip())
    # Extract the first balanced JSON object if possible.
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(cleaned[start:end + 1])

    last_error: Exception | None = None
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except Exception as err:
            last_error = err
            continue
    # If all attempts fail, raise the last error to trigger fallback.
    raise last_error or ValueError("Unable to parse challenge JSON response.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
