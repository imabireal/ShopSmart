from flask import Blueprint, request, jsonify, render_template, session
from flask_login import login_required, current_user
from app.chatbot.chatbot_service import ChatbotService
import logging

# Set up logging
logger = logging.getLogger('flask-ecommerce')

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize chatbot service
chatbot_service = ChatbotService()

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages and return product recommendations
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get user context if available (for personalized recommendations)
        user_id = str(current_user.id) if current_user.is_authenticated else None
        
        # Get chat history from session or create new
        chat_history = session.get('chat_history', [])
        
        # Get recommendations from chatbot service
        response = chatbot_service.get_recommendations(message, user_id, chat_history)
        
        # Update chat history
        chat_history.append({'user': message, 'bot': response['response']})
        session['chat_history'] = chat_history
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500

@chatbot_bp.route('/chat/clear', methods=['POST'])
def clear_chat():
    """
    Clear chat history from session
    """
    try:
        session.pop('chat_history', None)
        return jsonify({'success': True, 'message': 'Chat history cleared'})
    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to clear chat history'}), 500
