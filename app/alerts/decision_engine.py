class AlertDecisionEngine:
    """
    Determines whether a data quality alert should be triggered.

    Alert is generated if:
    1. Schema validation fails.
    2. Data quality score is below threshold.
    3. Any critical validation rule fails.
    """

    # Minimum acceptable quality score
    QUALITY_THRESHOLD = 90

    @classmethod
    def should_send_alert(
        cls,
        schema_status,
        validation_results,
        quality_score
    ):
        """
        Decide whether an alert should be sent.

        Parameters
        ----------
        schema_status : bool
            True if schema validation passed, False otherwise.

        validation_results : list
            List containing results of each validation rule.
            Each result is expected to have:
                - passed (bool)
                - severity (str)

        quality_score : float
            Overall data quality score (0-100).

        Returns
        -------
        bool
            True  -> Send alert
            False -> No alert required
        """

        # ---------------------------------------------------------
        # Step 1 : Check Schema Validation
        # If schema itself is invalid, immediately trigger an alert.
        # ---------------------------------------------------------
        if not schema_status:
            return True

        # ---------------------------------------------------------
        # Step 2 : Check Overall Data Quality Score
        # Trigger alert if score is below the configured threshold.
        # ---------------------------------------------------------
        if quality_score < cls.QUALITY_THRESHOLD:
            return True

        # ---------------------------------------------------------
        # Step 3 : Check Individual Validation Rules
        # Look for any failed rule with "Critical" severity.
        # ---------------------------------------------------------
        for result in validation_results:

            if (
                not result.passed and               # Rule failed
                result.severity.lower() == "critical"   # Critical rule
            ):
                return True

        # ---------------------------------------------------------
        # If none of the above conditions are met,
        # dataset is considered healthy.
        # ---------------------------------------------------------
        return False