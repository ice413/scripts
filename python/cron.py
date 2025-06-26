#!/usr/bin/env python3
#====================================================
# Script Name:   cron.py
# Description:   Create lines for crontab
# Author:        claes-nilsson
# Created:       2025-04-12 09:34:53
#====================================================

import os

def get_user_input(prompt):
    return input(prompt)

def add_cron_job():
    user = get_user_input("Which user? (root default): ") or "root"
    command = get_user_input("What should be executed? : ")
    schedule_type = get_user_input("Once or multiple times? (1. Once 2. Multiple): ")

    if schedule_type == '1':
        time = get_user_input("What time? (hh:mm): ")
        cron_time = f"{time.split(':')[1]} {time.split(':')[0]} * * *"
    else:
        days = []
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            if get_user_input(f"Run on {day}? (y/n): ").lower() == 'y':
                days.append(day[:3].upper())
        cron_time = f"* * * * {','.join(days)}"

    cron_job = f"{cron_time} {command}\n"

    current_crontab = os.popen(f'crontab -u {user} -l').read()
    new_crontab = current_crontab + cron_job

    with open('new_crontab.txt', 'w') as f:
        f.write(new_crontab)

    os.system(f'crontab -u {user} new_crontab.txt')
    os.remove('new_crontab.txt')

add_cron_job()

