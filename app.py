from flask import Flask, render_template, request

app = Flask(__name__)

MBTI_LIST = [
    "INFP", "ENFP", "INFJ", "ENFJ",
    "INTJ", "ENTJ", "INTP", "ENTP",
    "ISFP", "ESFP", "ISTP", "ESTP",
    "ISFJ", "ESFJ", "ISTJ", "ESTJ"
]

GENDER_WEIGHTS = {
    "male-male": {
        "compatibility": 0.40,
        "duration": 0.24,
        "recovery": 0.19,
        "expression": 0.17,
    },
    "male-female": {
        "compatibility": 0.40,
        "duration": 0.23,
        "recovery": 0.19,
        "expression": 0.18,
    },
    "male-none": {
        "compatibility": 0.40,
        "duration": 0.24,
        "recovery": 0.19,
        "expression": 0.17,
    },
    "female-male": {
        "compatibility": 0.40,
        "duration": 0.22,
        "recovery": 0.20,
        "expression": 0.18,
    },
    "female-female": {
        "compatibility": 0.40,
        "duration": 0.21,
        "recovery": 0.20,
        "expression": 0.19,
    },
    "female-none": {
        "compatibility": 0.40,
        "duration": 0.22,
        "recovery": 0.20,
        "expression": 0.18,
    },
}

GENDER_DESCRIPTIONS = {
    "male-male": "선택한 관계 유형을 기준으로 연애 궁합을 분석했어요.",
    "male-female": "선택한 관계 유형을 기준으로 연애 궁합을 분석했어요.",
    "male-none": "상대 성별을 반영하지 않고 본인 기준으로 연애 궁합을 분석했어요.",
    "female-male": "선택한 관계 유형을 기준으로 연애 궁합을 분석했어요.",
    "female-female": "선택한 관계 유형을 기준으로 연애 궁합을 분석했어요.",
    "female-none": "상대 성별을 반영하지 않고 본인 기준으로 연애 궁합을 분석했어요.",
}

COMPAT = {
    "INFP": {"ENFJ": 90, "ENTJ": 85, "INFJ": 80},
    "ENFP": {"INFJ": 90, "INTJ": 85, "INFP": 80},
    "INFJ": {"ENFP": 90, "ENTP": 85, "INFP": 80},
    "ENFJ": {"INFP": 90, "ISFP": 85, "ENFP": 80},

    "INTJ": {"ENFP": 85, "ENTP": 80, "INFJ": 75},
    "ENTJ": {"INFP": 85, "INTP": 80, "ENFP": 75},
    "INTP": {"ENTJ": 80, "ENFJ": 75, "INTJ": 70},
    "ENTP": {"INFJ": 85, "INTJ": 80, "ENFP": 75},

    "ISFP": {"ENFJ": 85, "ESFJ": 80, "INFP": 75},
    "ESFP": {"ISFJ": 80, "ISTJ": 75, "ENFP": 70},
    "ISTP": {"ESTJ": 80, "ESFJ": 75, "INTP": 70},
    "ESTP": {"ISFJ": 80, "ISTJ": 75, "ENTP": 70},

    "ISFJ": {"ESFP": 80, "ESTP": 80, "ISFP": 75},
    "ESFJ": {"ISFP": 80, "ISTP": 75, "ENFJ": 70},
    "ISTJ": {"ESFP": 75, "ESTP": 75, "ESTJ": 70},
    "ESTJ": {"ISTP": 80, "ISTJ": 70, "ENTJ": 70},
}


# 코드작성 1

def get_detail_scores(my_mbti):
    mbti_scores = list(COMPAT.get(my_mbti, {}).values())

    if not mbti_scores:
        return {
            "compatibility": 50,
            "duration": 50,
            "recovery": 50,
            "expression": 50,
        }

    sorted_scores = sorted(mbti_scores)
    middle_index = len(sorted_scores) // 2
    return {
        "compatibility": round(sum(mbti_scores) / len(mbti_scores)),
        "duration": max(mbti_scores),
        "recovery": min(mbti_scores),
        "expression": sorted_scores[middle_index],
    }


def get_best_matches(my_mbti):
    matches = COMPAT.get(my_mbti, {})
    return [
        mbti
        for mbti, _ in sorted(matches.items(), key=lambda item: item[1], reverse=True)[:3]
    ]


def normalize_partner_gender(partner_gender):
    if partner_gender not in ("male", "female", "none"):
        return "none"
    return partner_gender


def calculate_final_score(scores, my_gender, partner_gender):
    relation_key = f"{my_gender}-{partner_gender}"
    weights = GENDER_WEIGHTS.get(relation_key)

    if not weights:
        raise ValueError("올바르지 않은 성별 선택값입니다.")

    return round(
        scores["compatibility"] * weights["compatibility"]
        + scores["duration"] * weights["duration"]
        + scores["recovery"] * weights["recovery"]
        + scores["expression"] * weights["expression"]
    )

# 코드작성 2

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        my_mbti = request.form.get("my_mbti")
        my_gender = request.form.get("myGender")
        partner_gender = normalize_partner_gender(request.form.get("partnerGender", "none"))

        if my_gender not in ("male", "female"):
            error = "본인 성별을 선택해주세요."
        else:
            scores = get_detail_scores(my_mbti)
            score = calculate_final_score(scores, my_gender, partner_gender)
            stage = get_stage(score)
            description = GENDER_DESCRIPTIONS[f"{my_gender}-{partner_gender}"]

            result = {
                "my_mbti": my_mbti,
                "my_gender": my_gender,
                "partner_gender": partner_gender,
                "score": score,
                "best_matches": get_best_matches(my_mbti),
                "stage": stage,
                "description": description,
            }

    return render_template(
        "index.html",
        mbti_list=MBTI_LIST,
        error=error,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True, port=1234)

'''
def get_score(my_mbti):
    scores = COMPAT.get(my_mbti, {}).values()
    if not scores:
        return 50
    return round(sum(scores) / len(scores))

def get_stage(score):
    if score >= 90:
        return "운명 궁합"
    elif score >= 80:
        return "좋은 궁합"
    elif score >= 70:
        return "무난한 궁합"
    elif score >= 60:
        return "노력형 궁합"
    else:
        return "조심할 궁합"
'''