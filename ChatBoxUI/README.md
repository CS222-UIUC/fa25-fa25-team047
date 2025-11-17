
  # AI Prompting Page Design

  This is a code bundle for AI Prompting Page Design. The original project is available at https://www.figma.com/design/Pd2r5N7iFjUn0jEs6dOK9r/AI-Prompting-Page-Design.

  ## Running the code

  1. **Install dependencies:**
     ```bash
     npm i
     ```

  2. **Start the backend Flask server** (in a separate terminal):
     ```bash
     cd ../flask
     pip install -r requirements.txt
     # Create .env file with OPENAI_API_KEY=your_key_here
     python app.py
     ```

  3. **Start the frontend development server:**
     ```bash
     npm run dev
     ```

  The app will be available at `http://localhost:3000`

  ## Features

  - User authentication
  - Real-time chat with ChatGPT API
  - Message history display
  - File attachments support
  - Modern UI with shadcn/ui components
  