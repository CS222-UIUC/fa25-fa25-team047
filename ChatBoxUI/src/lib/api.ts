const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export async function sendChatMessage(message: string, history: ChatMessage[]): Promise<string> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        history,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(errorData.error || 'Failed to send message');
    }

    const data = await response.json();
    return data.message;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
}

