"""Require every processed resource to be linked from a same-domain MOC."""

from check_moc_coverage import main as check_coverage


def main():
    return check_coverage(folder="90 - Resources", note_label="processed resources")


if __name__ == "__main__":
    raise SystemExit(main())
