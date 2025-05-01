import sqlite3
from hashlib import sha256
from typing import List, Tuple, Optional, Any

def init_db():
    """Initialize the database with required tables"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    
    # Students table
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                std_id TEXT UNIQUE, 
                firstname TEXT NOT NULL,
                surname TEXT NOT NULL,
                dob TEXT,
                age INTEGER,
                gender TEXT,
                mobile TEXT)""")  # Removed address field
    
    # Users table with role-based access
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'user')))""")
    
    # Create default admin if not exists
    cur.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
    if cur.fetchone()[0] == 0:
        hashed = sha256("admin123".encode()).hexdigest()
        cur.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
                   ("admin", hashed, "admin"))
    
    con.commit()
    con.close()

# ===== User Management =====
def add_user(username: str, password: str, role: str) -> bool:
    """Add a new user to the system"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    hashed = sha256(password.encode()).hexdigest()
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
                   (username, hashed, role))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()

def get_users() -> List[Tuple]:
    """Get all users from the system"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    cur.execute("SELECT id, username, role FROM users")
    users = cur.fetchall()
    con.close()
    return users

def delete_user(user_id: int) -> bool:
    """Delete a user from the system"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        con.commit()
        return cur.rowcount > 0
    finally:
        con.close()

def authenticate(username: str, password: str) -> Optional[str]:
    """Authenticate a user and return their role"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    hashed = sha256(password.encode()).hexdigest()
    cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hashed))
    result = cur.fetchone()
    con.close()
    return result[0] if result else None

# ===== Student Management =====
def add_student(std_id: str, firstname: str, surname: str, dob: str, 
               age: int, gender: str, mobile: str) -> bool:  # Removed address parameter
    """Add a new student record"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    try:
        cur.execute("""INSERT INTO students 
                    (std_id, firstname, surname, dob, age, gender, mobile)
                    VALUES (?,?,?,?,?,?,?)""",
                   (std_id, firstname, surname, dob, age, gender, mobile))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()

def get_students() -> List[Tuple]:
    """Get all student records"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    con.close()
    return students

def search_students(**kwargs) -> List[Tuple]:
    """Search students with flexible criteria"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    
    conditions = []
    params = []
    for field, value in kwargs.items():
        if value:
            conditions.append(f"{field} LIKE ?")
            params.append(f"%{value}%")
    
    query = "SELECT * FROM students"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    cur.execute(query, params)
    results = cur.fetchall()
    con.close()
    return results

def update_student(student_id: int, **kwargs) -> bool:
    """Update a student record"""
    if not kwargs:
        return False
    
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    
    set_clause = ", ".join([f"{k}=?" for k in kwargs])
    values = list(kwargs.values())
    values.append(student_id)
    
    try:
        cur.execute(f"UPDATE students SET {set_clause} WHERE id=?", values)
        con.commit()
        return cur.rowcount > 0
    finally:
        con.close()

def delete_student(student_id: int) -> bool:
    """Delete a student record"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM students WHERE id=?", (student_id,))
        con.commit()
        return cur.rowcount > 0
    finally:
        con.close()

# Initialize the database
init_db()