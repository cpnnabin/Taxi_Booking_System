import mysql.connector

def update_database():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="CPNnabin@2004dhakal",
            database="taxi_booking_system_test"
        )
        cursor = conn.cursor()
        
        print("Connected to database successfully!")
        
        # Add driver_id column to bookings table if it doesn't exist
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'taxi_booking_system_test' 
            AND TABLE_NAME = 'bookings' 
            AND COLUMN_NAME = 'driver_id'
        """)
        
        if not cursor.fetchone():
            print("Adding driver_id column to bookings table...")
            cursor.execute("""
                ALTER TABLE bookings 
                ADD COLUMN driver_id INT NULL,
                ADD FOREIGN KEY (driver_id) REFERENCES drivers(DID)
                ON DELETE SET NULL
            """)
            print("Successfully added driver_id column to bookings table.")
        else:
            print("driver_id column already exists in bookings table.")
        
        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()
        print("Database update completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    update_database()
    input("Press Enter to exit...")
