import argparse
import pandas as pd
from pathlib import Path
import calendar
from paceutils import Helpers

auditor_dict = {
    "documentation": ["Yenissa", "Adrianna"],
    "cos": ["Betsy"],
    "closed": ["Betsy", "Dr. G", "Julianne", "Mike", "Liz"],
    "initial": ["Cherie", "Melisa"],
}


def get_sample(start_date=None, end_date=None, audit_type="documentation"):
    helper = Helpers()

    if (start_date is None) | (end_date is None):
        if audit_type == "cos":
            dates = helper.last_three_months()
        else:
            dates = helper.last_month()
        start_date = dates[0]
        end_date = dates[1]
        current_date = helper.month_to_date()[1]
    else:
        current_date = end_date

    if audit_type == "initial":
        cps = pd.read_csv(
            "./data/ParticipantCarePlanReview.csv", parse_dates=["StatusDate"]
        )
        sample = cps[
            (cps.StatusDate >= pd.to_datetime(start_date))
            & (cps.StatusDate <= pd.to_datetime(end_date))
            & (cps.Type == "Initial")
        ].copy()
        filename = "initial_cp_all_"

    if audit_type == "cos":
        cps = pd.read_csv(
            "./data/ParticipantCarePlanReview.csv", parse_dates=["StatusDate"]
        )
        sample = cps[
            (cps["Type"] == "Change in Condition")
            & (cps.StatusDate >= pd.to_datetime(start_date))
            & (cps.StatusDate <= pd.to_datetime(end_date))
        ].copy()
        filename = "cos_cp_"

    if audit_type == "closed":
        cps = pd.read_csv(
            "./data/ParticipantCarePlanReview.csv", parse_dates=["StatusDate"]
        )
        sample = cps[
            (cps.StatusDate >= pd.to_datetime(start_date))
            & (cps.StatusDate <= pd.to_datetime(end_date))
            & (cps.Type != "Initial")
        ].copy()
        filename = "careplan_audit_"

        sample = sample.sample(frac=0.3)

    if audit_type == "documentation":
        query = """SELECT e.member_id, enrollment_date, first, last
                    FROM enrollment e JOIN ppts p ON e.member_id=p.member_id
                    WHERE (disenrollment_date >= ? OR disenrollment_date IS NULL)
                    AND enrollment_date <= ?;"""
        sample = helper.dataframe_query(query, params=(start_date, end_date)).sample(
            frac=0.04
        )
        filename = "documentation_audit_"

    sample.reset_index(drop=True, inplace=True)

    auditors = auditor_dict[audit_type]
    sample["auditor"] = ""
    sample_size = sample.shape[0]
    num_auditors = len(auditors)

    splits = [
        sample_size // num_auditors + (1 if x < sample_size % num_auditors else 0)
        for x in range(num_auditors)
    ]

    start = 0
    for auditor, split in zip(auditors, splits):
        sample.loc[start : start + split, "auditor"] = auditor
        start += split

    sample["audit_number"] = range(1, sample_size + 1)

    cols = ["audit_number", "auditor"] + [
        col for col in sample.columns if col not in ["audit_number", "auditor"]
    ]
    sample = sample[cols].copy()

    month = int(current_date.split("-")[1])
    year = current_date.split("-")[0]
    month_name = calendar.month_name[month]

    sample_folder = Path(f"V:/CMT/_Audits/{month}_{month_name} {year}/Ppt Samples")
    file_to_save = sample_folder / f"{filename}{start_date}_{end_date}.csv"

    sample.to_csv(file_to_save, index=False)

    print("Success")


def samples_wrapper(start_date=None, end_date=None, audit_type="all"):
    if audit_type == "all":
        for sample in ["initial", "cos", "closed", "documentation"]:
            get_sample(start_date, end_date, audit_type=sample)
        print("Success")
    else:
        get_sample(start_date, end_date, audit_type=audit_type)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start_date",
        default=None,
        help="start of the audit-does not need to be specified for standard audit.",
    )

    parser.add_argument(
        "--end_date",
        default=None,
        help="start of the audit-does not need to be specified for standard audit.",
    )

    parser.add_argument(
        "--audit_type",
        default="all",
        help="Defaults to all to run all audits, can be specified to only run one sample of initial, cos, closed, or documentation",
    )

    arguments = parser.parse_args()

    samples_wrapper(**vars(arguments))
