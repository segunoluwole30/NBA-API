import csv
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Player

def import_players_from_csv(file_path: str):
    """
    Import players from a CSV file into the database.
    :param file_path: Path to the CSV file.
    """
    # Create a new session
    db: Session = SessionLocal()

    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                player = Player(
                    name=row['name'],
                    position=row['position'],
                    team=row['team'],
                    age=int(row['age']),
                    points_per_game=float(row['points_per_game']),
                    assists_per_game=float(row['assists_per_game']),
                    rebounds_per_game=float(row['rebounds_per_game'])
                )
                db.add(player)
            db.commit()
            print("Players imported successfully.")
    except Exception as e:
        print(f"Error importing players: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_players_from_csv('active_players.csv')