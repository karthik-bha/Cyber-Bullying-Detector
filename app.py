from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from tensorflow.keras.models import load_model
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app)

# Load the pre-trained model and tokenizer
model = load_model("cyberbullying_detection_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Function to preprocess text for model
def preprocess_text(text):
    sequences = tokenizer.texts_to_sequences([text])
    padded_seq = pad_sequences(sequences, maxlen=128)
    return padded_seq

@app.route('/')
def chat():
    return render_template('chat.html')

# WebSocket handler for receiving messages
@socketio.on('message')
def handle_socket_message(data):
    text = data['message']
    user = data['user']

    # Preprocess and predict if the message is cyberbullying
    preprocessed_text = preprocess_text(text)
    prediction = model.predict(preprocessed_text)[0][0]
    is_cyberbullying = prediction > 0.5
    result = "Cyberbullying Detected" if is_cyberbullying else "No Cyberbullying Detected"

    # Emit the message and result back to all connected clients
    emit('message', {'message': text, 'user': user, 'cyberbullying': result}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
