def parse_log_line(line):
    
    try:
      
        parts = line.strip().split(None, 4)
        
        if len(parts) < 5:
            raise ValueError("Line doesn't have enough parts")

        timestamp_str = parts[0] + " " + parts[1]
        level = parts[2]
        component = parts[3]
        message = parts[4]

        return timestamp_str, level, component, message

    except Exception as e:
        print(f"Error parsing line: {line}")
        print(f"Reason: {e}")
        return None

