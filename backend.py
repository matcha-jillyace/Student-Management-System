import sqlite3
from hashlib import sha256
from typing import List, Tuple, Optional

def init_db():
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                std_id TEXT UNIQUE, 
                fullname TEXT NOT NULL,
                course TEXT,
                section TEXT,
                dob TEXT,
                gender TEXT,
                mobile TEXT)""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'user')))""")
    
    cur.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
    if cur.fetchone()[0] == 0:
        hashed = sha256("admin123".encode()).hexdigest()
        cur.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
                   ("admin", hashed, "admin"))
    
    con.commit()
    con.close()

# ===== User Management =====
def add_user(username, password, role):
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

# ===== Updated Student Management =====
def add_student(std_id: str, fullname: str, course: str, section: str, 
                dob: str, gender: str, mobile: str) -> bool:
    """Add a new student record with updated fields"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    try:
        cur.execute("""INSERT INTO students 
                    (std_id, fullname, course, section, dob, gender, mobile)
                    VALUES (?,?,?,?,?,?,?)""",
                   (std_id, fullname, course, section, dob, gender, mobile))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()

def get_students() -> List[Tuple]:
    """Get all student records with new structure"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    con.close()
    return students

def search_students(**kwargs) -> List[Tuple]:
    """Search students with flexible criteria using new fields"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    conditions = []
    params = []
    valid_fields = ['std_id', 'fullname', 'course', 'section', 'dob', 'gender', 'mobile']
    
    for field, value in kwargs.items():
        if value and field in valid_fields:
            conditions.append(f"{field} LIKE ?")
            params.append(f"%{value}%")
    
    query = "SELECT * FROM students"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    cur.execute(query, params)
    results = cur.fetchall()
    con.close()
    return results

def update_student(student_id: int, **kwargs):
    """Update a student record with new fields"""
    valid_fields = ['std_id', 'fullname', 'course', 'section', 'dob', 'gender', 'mobile']
    updates = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
    
    if not updates:
        return False
    
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    
    set_clause = ", ".join([f"{k}=?" for k in updates])
    values = list(updates.values())
    values.append(student_id)
    
    try:
        cur.execute(f"UPDATE students SET {set_clause} WHERE id=?", values)
        con.commit()
        return cur.rowcount > 0
    finally:
        con.close()

def delete_student(student_id: int):
    """Delete a student record"""
    con = sqlite3.connect("school.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM students WHERE id=?", (student_id,))
        con.commit()
        return cur.rowcount > 0
    finally:
        con.close()

init_db()



