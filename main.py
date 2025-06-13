from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional 
from pydantic import BaseModel
import os 
from d import parse_log_line
import uuid
from datetime import datetime
from contextlib import asynccontextmanager

LOG_DIRECTORY = "logs"

app = FastAPI()

class LogEntry(BaseModel):
        id:str
        timestamp : datetime
        level : str
        component : str
        message : str

log_entries : List[LogEntry] = []

def parse_log_entries():
        global log_entries
        log_entries.clear()

        for filename in os.listdir(LOG_DIRECTORY):
                filepath = os.path.join(LOG_DIRECTORY,filename)
                print(filepath)
                with open(filepath, "r") as file:
                        for line in file.readlines():
                                try:
                                        print(line)
                                        parts = parse_log_line(line)
                                        print(parts)
                                        if len(parts) == 4:
                                                timestamp, level, component, message=parts
                                                log_entry = LogEntry(
                                                        id=str(uuid.uuid4()),
                                                        timestamp=datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S"),
                                                        level = level,
                                                        component=component,
                                                        message=message
                                                )
                                                log_entries.append(log_entry)
                                                print(log_entries)
                                except Exception:
                                        continue

@asynccontextmanager
async def lifespan(app: FastAPI):
    parse_log_entries()
    yield
app = FastAPI(lifespan=lifespan)
@app.get("/logs",response_model=List[LogEntry])

def get_logs(
                level : Optional[str] = None,
                component : Optional[str] = None,
                start_time : Optional[str] = None,
                end_time: Optional[str] = None,
):
        filtered_logs = log_entries
        if level: 
                filtered_logs = [log for log in filtered_logs if log.level == level]
        
        if component:
                filtered_logs=[log for log in filtered_logs if log.component == component]

        if start_time:
                try:
                        start_dt = datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")
                        filtered_logs = [log for log in filtered_logs if log.timestamp >= start_dt]
                except ValueError:
                        raise HTTPException(status_code=400, detail="Invalid start_time format")
                
        if end_time:
                try:
                        end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                        filtered_logs = [log for log in filtered_logs if log.timestamp <= end_dt]
                
                except ValueError:
                        raise HTTPException(status_code=400, detail="Invalid end_time format")
        
        return filtered_logs

@app.get("/logs/stats")
def get_stats():
        total = len(log_entries)
        level_counts = {}
        component_count = {}

        for log in log_entries:
                level_counts[log.level] = level_counts.get(log.level,0)+1
                component_count[log.component] = component_count.get(log.component,0)+1

        return{
                "total_count" : total,
                "logs_per_level" : level_counts,
                "logs_per_components" : component_count
            }

@app.get("/logs/{log_id}")

def get_log_by_id(log_id:str):
        for log in log_entries:
                if log.id == log_id:
                        return log
        raise HTTPException(status_code=404, detail="Log not found")