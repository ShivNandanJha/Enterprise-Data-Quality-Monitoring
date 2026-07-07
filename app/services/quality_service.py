class QualityService:

    weights = {

        "critical":10,

        "warning":5,

        "info":1

    }
    
# Start
# 100
# ↓
# Every failed Critical
# -10
# ↓
# Every failed Warning
# -5
# ↓
# Minimum = 0

    @classmethod

    def calculate(cls, results):

        score = 100

        for r in results:

            if not r.passed:

                score -= cls.weights.get(

                    r.severity.lower(),

                    1

                )

        return max(score,0)