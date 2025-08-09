from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# روابط API الجديدة
LIKE_API = "http://160.250.137.144:5001/like"  # API اللايكات الجديد
INFO_API = "https://rzx-api-info-bot-ob15.onrender.com/"  # API المعلومات الجديد

@app.route('/like', methods=['GET'])
def like():
    uid = request.args.get('uid')
    server_name = request.args.get('server_name')

    if not uid or not server_name:
        return jsonify({"error": "Parameters 'uid' and 'server_name' are required."}), 400

    if not uid.isdigit():
        return "Make sure the ID is correct", 400

    try:
        # جلب معلومات اللاعب
        info_response = requests.get(f"{INFO_API}{uid}")
        if info_response.status_code != 200:
            return f"Failed to get info for user {uid}", 500

        info_data = info_response.json()
        basic = info_data.get("basicinfo", [{}])[0]

        name = basic.get("username", "Unknown")
        level = basic.get("level", "N/A")
        region = basic.get("region", server_name)
        likes_before = basic.get("likes", 0)
        owner = info_data.get("Owners", ["@Unknown"])[0]

        # إرسال اللايكات
        like_response = requests.get(LIKE_API, params={
            "uid": uid,
            "server_name": region,
            "key": "tanhungvip11231"
        })
        if like_response.status_code != 200:
            return f"Failed to send likes to user {uid}", 500

        like_data = like_response.json()
        likes_added = like_data.get("LikesafterCommand", likes_before) - likes_before
        likes_after = like_data.get("LikesafterCommand", likes_before)

        # النتيجة
        result = f"""[✓] Likes Sent:
- UID: {uid}
- Name: {name}
- Region: {region}
- Level: {level}
- Likes Before: {likes_before}
- Likes After: {likes_after}
- Likes Added: {likes_added}

DEV API: {owner}
"""
        return result, 200, {"Content-Type": "text/plain; charset=utf-8"}

    except Exception:
        return f"Failed to send likes to user {uid}", 500


if __name__ == '__main__':
    app.run(debug=True)
