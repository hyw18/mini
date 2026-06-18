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


# 아래에 두 개의 함수를 작성하세요.
#
# 1. 첫 번째 함수
#    - 두 MBTI 값을 받아 궁합 점수를 반환합니다.
#    - 두 MBTI가 같으면 정해진 기본 점수를 반환합니다.
#    - COMPAT 점수표에 조합이 있으면 그 점수를 사용합니다.
#    - 점수표에 없는 조합이면 무난한 기본 점수를 반환합니다.
#
# 2. 두 번째 함수
#    - 점수를 받아 궁합 결과를 반환합니다.
#    - 반환값은 이모지, 궁합 이름, 설명문 3개입니다.
#    - 높은 점수일수록 더 좋은 궁합 결과가 나오도록 조건문을 사용합니다.
#
# 코드 입력


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