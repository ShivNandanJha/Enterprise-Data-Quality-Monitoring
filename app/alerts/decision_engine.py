class AlertDecisionEngine:

    QUALITY_THRESHOLD = 90

    @classmethod
    def should_send_alert(
        cls,
        schema_status,
        validation_results,
        quality_score
    ):

        # Schema failure
        if not schema_status:
            return True

        # Quality Score
        if quality_score < cls.QUALITY_THRESHOLD:
            return True

        # Critical Rule Failure
        for result in validation_results:

            if (
                not result.passed
                and result.severity.lower() == "critical"
            ):
                return True

        return False