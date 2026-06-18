from flask import Flask, render_template, request

app = Flask(__name__)

MBTIS = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

COMPAT = {
    "INFP": {"ENFJ": 95, "ENTJ": 90, "ESTJ": 60},
    "ENFJ": {"INFP": 95, "ISFP": 85, "ISTP": 55},
    "INTJ": {"ENFP": 92, "ENTP": 88, "ESFP": 55},
    "ENFP": {"INTJ": 92, "INFJ": 90, "ISTJ": 60},
    "ISTJ": {"ESFP": 80, "ESTJ": 75, "ENFP": 60},
    "ESFP": {"ISTJ": 80, "ISFJ": 78, "INTJ": 55},
}


def get_score(mbti1, mbti2):
    if mbti1 == mbti2:
        return 75
    return COMPAT.get(mbti1, {}).get(mbti2, 50)


def get_stage(score):
    if score >= 90:
        return "❤️", "운명 궁합", "서로의 장점이 잘 살아나는 조합이에요."
    elif score >= 80:
        return "😊", "찰떡 궁합", "성향 차이도 매력으로 느껴질 수 있어요."
    elif score >= 70:
        return "🙂", "좋은 궁합", "서로를 이해하면 오래 가기 좋은 조합이에요."
    else:
        return "😐", "무난한 궁합", "천천히 맞춰가면 괜찮은 조합이에요."


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        mbti1 = request.form.get("mbti1")
        mbti2 = request.form.get("mbti2")
        expected_score = request.form.get("expected_score", "0")

        score = get_score(mbti1, mbti2)
        emoji, label, description = get_stage(score)

        expected = float(expected_score)
        difference = abs(score - expected)

        result = {
            "mbti1": mbti1,
            "mbti2": mbti2,
            "score": score,
            "expected": expected,
            "difference": difference,
            "emoji": emoji,
            "label": label,
            "description": description,
        }

    return render_template("index.html", mbtis=MBTIS, result=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1234)