from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging (sensitive data should not be logged)
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1002351667124")
MESSAGE_THREAD_ID = os.getenv("MESSAGE_THREAD_ID", "59")
USER_ID_LANA = os.getenv("USER_ID_LANA", "7122508724")

# Ensure required environment variables are set
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is not set in the environment.")

# Telegram API URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Log environment values (excluding sensitive ones)
logging.debug(f"✅ TELEGRAM_CHAT_ID: {TELEGRAM_CHAT_ID}")
logging.debug(f"✅ MESSAGE_THREAD_ID: {MESSAGE_THREAD_ID}")
logging.debug(f"✅ USER_ID_LANA: {USER_ID_LANA}")


@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        if not request.is_json:
            logging.warning("❌ Invalid request: Content-Type must be application/json")
            return jsonify({"success": False, "error": "Invalid content type, expecting JSON"}), 400

        # Get JSON data from request
        data = request.json
        logging.debug(f"📩 Received data: {data}")

        # Validate required fields (eld removed)
        required_fields = ["name", "dateFrom", "dateTill", "reason", "truckNumber", "company", "pauseInsuranceEld"]
        if not all(field in data and data[field] for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            logging.warning(f"❌ Missing or invalid fields: {missing_fields}")
            return jsonify({"success": False, "error": f"Missing or invalid fields: {missing_fields}"}), 400

        # Extract values (eld removed)
        name = data["name"]
        truck_number = data["truckNumber"]
        company = data["company"]
        date_from = data["dateFrom"]
        date_till = data["dateTill"]
        reason = data["reason"]
        pause_insurance_eld = data["pauseInsuranceEld"]

        # Construct the message for Telegram (eld removed)
        message = (
            f"📝 *TIME-OFF REQUEST* \n\n"
            f"🔹 *Name:* {name}\n"
            f"🔹 *Truck Number:* {truck_number}\n"
            f"🔹 *Company:* {company}\n"
            f"🔹 *Date Off:* From {date_from} till {date_till}\n"
            f"🔹 *Reason:* {reason}\n"
            f"🔹 *Pause Insurance and ELD?:* {pause_insurance_eld}\n\n"
            f"⚠️ The driver {name} will be back to work on {date_till}."
        )

        # Send message to Telegram group
        payload_group = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "message_thread_id": int(MESSAGE_THREAD_ID)
        }

        response = requests.post(TELEGRAM_API_URL, json=payload_group)
        logging.debug(f"📨 Telegram Group Response: {response.status_code} {response.text}")
        response.raise_for_status()

        # Send a message to Lana (eld mention removed)
        payload_lana = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"Good day [Lana](tg://user?id={USER_ID_LANA})! "
                    f"Please check the time-off request for driver {name}. "
                    f"They will be back on {date_till}. Thank you!",
            "parse_mode": "Markdown",
            "message_thread_id": int(MESSAGE_THREAD_ID)
        }
        response_lana = requests.post(TELEGRAM_API_URL, json=payload_lana)
        logging.debug(f"📨 Telegram Lana Response: {response_lana.status_code} {response_lana.text}")

        if not response_lana.ok:
            logging.error(f"❌ Error sending message to Lana: {response_lana.text}")
            return jsonify({"success": False, "error": "Failed to notify Lana."}), 500

        return jsonify({"success": True, "message": "Your request has been sent successfully!"})

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Telegram API error: {str(e)}")
        return jsonify({"success": False, "error": f"Telegram API error: {str(e)}"}), 500
    except Exception as e:
        logging.error(f"❌ Server error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
