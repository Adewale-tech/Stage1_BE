from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
import hashlib
import json
import os

app = FastAPI()

DATA_FILE = "data.json"

# Load or initialize data file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class StringInput(BaseModel):
    value: str

@app.post("/strings", status_code=201)
def analyze_string(payload: StringInput):
    value = payload.value.strip()
    if not value:
        raise HTTPException(status_code=400, detail="Value cannot be empty")

    # Compute properties
    sha_hash = hashlib.sha256(value.encode()).hexdigest()
    data = load_data()

    # Check if string already exists
    for item in data:
        if item["id"] == sha_hash:
            raise HTTPException(status_code=409, detail="String already exists")

    properties = {
        "length": len(value),
        "is_palindrome": value.lower() == value[::-1].lower(),
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "sha256_hash": sha_hash,
        "character_frequency_map": {c: value.count(c) for c in set(value)}
    }

    entry = {
        "id": sha_hash,
        "value": value,
        "properties": properties,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    data.append(entry)
    save_data(data)

    return entry

@app.get("/strings/{string_value}")
def get_string(string_value: str):
    data = load_data()
    for item in data:
        if item["value"] == string_value:
            return item
    raise HTTPException(status_code=404, detail="String not found")

@app.get("/strings")
def get_all_strings(
    is_palindrome: bool = None,
    min_length: int = None,
    max_length: int = None,
    word_count: int = None,
    contains_character: str = None
):
    data = load_data()
    filtered = data

    if is_palindrome is not None:
        filtered = [d for d in filtered if d["properties"]["is_palindrome"] == is_palindrome]
    if min_length:
        filtered = [d for d in filtered if d["properties"]["length"] >= min_length]
    if max_length:
        filtered = [d for d in filtered if d["properties"]["length"] <= max_length]
    if word_count:
        filtered = [d for d in filtered if d["properties"]["word_count"] == word_count]
    if contains_character:
        filtered = [d for d in filtered if contains_character in d["value"]]

    return {
        "data": filtered,
        "count": len(filtered),
        "filters_applied": {
            "is_palindrome": is_palindrome,
            "min_length": min_length,
            "max_length": max_length,
            "word_count": word_count,
            "contains_character": contains_character
        }
    }

@app.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str):
    data = load_data()
    new_data = [d for d in data if d["value"] != string_value]

    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="String not found")

    save_data(new_data)
    return None
