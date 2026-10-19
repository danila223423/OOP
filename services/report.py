from models.user import User


def save_report(users: list[User], filename: str = "report.txt") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("+--- | login | time_in | time_out |\n")
        f.write("|---|---|---|\n")
        for user in users:
            if user.time_out is None:
                user.logout()
            f.write(
                f"| {user.login} "
                f"| {user.time_in:%d.%m.%Y %H:%M:%S} "
                f"| {user.time_out:%d.%m.%Y %H:%M:%S} |\n"
            )
        f.write("+---\n")