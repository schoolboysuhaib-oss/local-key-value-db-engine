"""
=============================================================================
PROJECT:  CUSTOM LIGHTWEIGHT KEY-VALUE LOG DATABASE ENGINE (V1.0.0-PROD)
TARGET:   Python 3.9+ Runtime Environment
PARADIGM: Object-Oriented Programming (OOP) & Disk Serialization Persistence
=============================================================================
"""

import os

class LocalDBEngine:
    """
    An immutable append-only log storage engine utilizing an in-memory
    dictionary hash-index map for sub-millisecond retrieval optimization.
    """
    def __init__(self, storage_filename: str = "db_store.log"):
        self.storage_filename = storage_filename
        self.memory_index = {}
        self._reconstruct_index_from_disk()

    def set_key_value(self, key: str, value: str) -> bool:
        """Appends records to the disk log file and updates the map index."""
        clean_key = str(key).strip()
        clean_value = str(value).strip()
        
        if not clean_key or "," in clean_key:
            print("[ERROR] Keys must be non-empty strings and cannot contain commas.")
            return False

        record_entry = f"{clean_key},{clean_value}\n"
        
        with open(self.storage_filename, "a", encoding="utf-8") as disk_file:
            disk_file.seek(0, os.SEEK_END)
            byte_offset_position = disk_file.tell()
            disk_file.write(record_entry)
            
            line_bytes_count = len(record_entry.encode("utf-8"))
            self.memory_index[clean_key] = (byte_offset_position, line_bytes_count)
            
        return True

    def get_value(self, key: str) -> str:
        """Queries the in-memory map to seek directly to disk offsets."""
        clean_key = str(key).strip()
        
        if clean_key not in self.memory_index:
            return None
            
        byte_offset, _ = self.memory_index[clean_key]
        
        with open(self.storage_filename, "r", encoding="utf-8") as disk_file:
            disk_file.seek(byte_offset)
            target_line = disk_file.readline().strip()
            
            if "," in target_line:
                _, stored_value = target_line.split(",", 1)
                return stored_value
                
        return None

    def _reconstruct_index_from_disk(self):
        """Parses log lines on bootup to safely reconstruct index mappings."""
        if not os.path.exists(self.storage_filename):
            return

        current_byte_offset = 0
        with open(self.storage_filename, "r", encoding="utf-8") as disk_file:
            for line in disk_file:
                line_bytes_count = len(line.encode("utf-8"))
                stripped_line = line.strip()
                if "," in stripped_line:
                    key, _ = stripped_line.split(",", 1)
                    self.memory_index[key] = (current_byte_offset, line_bytes_count)
                current_byte_offset += line_bytes_count

def main():
    """Interactive loop to interface with the core LocalDBEngine layers."""
    db = LocalDBEngine()
    
    print("\n=====================================================================")
    print("SYSTEM ACTIVE: CUSTOM KEY-VALUE APPEND-ONLY LOG DATABASE MATRIX V1.0")
    print("=====================================================================")
    print("Available Commands:  SET [key] [value]  |  GET [key]  |  EXIT")
    print("=====================================================================\n")

    while True:
        try:
            user_input = input("LocalDBEngine >> ").strip()
            if not user_input:
                continue
                
            input_parts = user_input.split(" ", 2)
            command = input_parts[0].upper()

            if command == "EXIT":
                print("Shutting down database pipelines safely. Exiting loop routine.")
                break
                
            elif command == "SET":
                if len(input_parts) < 3:
                    print("[ERROR] Syntax Invalid. Required format: SET [key] [value]")
                    continue
                key_arg = input_parts[1]
                value_arg = input_parts[2]
                if db.set_key_value(key_arg, value_arg):
                    print(f"[SUCCESS] Key '{key_arg}' committed to log offsets.")
                    
            elif command == "GET":
                if len(input_parts) < 2:
                    print("[ERROR] Syntax Invalid. Required format: GET [key]")
                    continue
                key_arg = input_parts[1]
                retrieved_value = db.get_value(key_arg)
                if retrieved_value is not None:
                    print(f"Value: {retrieved_value}")
                else:
                    print(f"[NOTICE] Key '{key_arg}' not found within index maps.")
            else:
                print("[ERROR] Unknown command intercept. Use SET, GET, or EXIT.")
        except Exception as error_intercept:
            print(f"[CRITICAL ERROR] Loop failure mode: {error_intercept}")

if __name__ == "__main__":
    main()
