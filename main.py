"""Entrypoint for the project."""
from config import settings


def main():
    print("Project skeleton running. DEBUG=", settings.get("DEBUG"))


if __name__ == "__main__":
    main()
