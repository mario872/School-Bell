import PySimpleGUI as GUI
from datetime import datetime as dt
from datetime import date

import yaml

with open('settings.yaml') as settings_yaml:
        settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)
        settings_yaml.close()

GUI.theme(settings['colour-theme'])

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

layout = [[GUI.Text('Days Left Until End of School Year:'), GUI.Text(size=(12,1), key='DAYS-LEFT')],
          [GUI.Text('Minutes Left of School Year:'), GUI.Text(size=(12,1), key='MINUTES-LEFT')],
          [GUI.Text('Seconds Left of School Year:'), GUI.Text(size=(12,1), key='SECONDS-LEFT')],
          [GUI.Text('')],
          [GUI.Text('Minutes Left of School Today: '), GUI.Text(size=(12,1), key='MINUTES-LEFT-TODAY')],
          [GUI.Text('Seconds Left of School Today:'), GUI.Text(size=(12,1), key='SECONDS-LEFT-TODAY'), GUI.Button('Open Settings', key='settings-button')]]

window = GUI.Window('Depressing', layout, finalize=True)

def open_settings():
    with open('settings.yaml') as settings_yaml:
        settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)
        settings_yaml.close()
    
    layout = [[GUI.Text("End of Day Hour"), GUI.Text("                                                                              End of Day Minute")],
              [GUI.Text("Monday: "), GUI.InputText("", key='monday-hour'), GUI.InputText("", key='monday-minute')],
              [GUI.Text("Tuesday: "), GUI.InputText("", key='tuesday-hour'), GUI.InputText("", key='tuesday-minute')],
              [GUI.Text("Wednesday: "), GUI.InputText("", key='wednesday-hour'), GUI.InputText("", key='wednesday-minute')],
              [GUI.Text("Thursday: "), GUI.InputText("", key='thursday-hour'), GUI.InputText("", key='thursday-minute')],
              [GUI.Text("Friday: "), GUI.InputText("", key='friday-hour'), GUI.InputText("", key='friday-minute')],
              [GUI.Text('')],
              [GUI.Text('Last Day of School Day: '), GUI.InputText('', key='last-day-day')],
              [GUI.Text('Last Day of School Month: '), GUI.InputText('', key='last-day-month')],
              [GUI.Text('')],
              [GUI.Text('Colour Theme: '), GUI.InputText('', key='colour-theme'), GUI.Button('Open Colour Theme Browser')],
              [GUI.Text('Close and reopen app to see changes after pressing button -->'), GUI.Button('Submit')]]
    
    window = GUI.Window("Settings", layout, modal=True, finalize=True)
    event, values = window.read(timeout=1)
    iter = 0
    for settings_option in settings:
        window[list(settings.keys())[iter]].update(str(settings[list(settings.keys())[iter]]))
        iter += 1
        
    while True:
        event, values = window.read()
        if event == "Exit" or event == GUI.WIN_CLOSED:
            break
        if event == 'Open Colour Theme Browser':
            GUI.theme_previewer()
        if event == 'Submit':
            settings = {}
            for settings_option in list(values.keys()):
                settings[settings_option] = values[settings_option]
            with open('settings.yaml', 'w') as settings_yaml:
                data = yaml.dump(settings, settings_yaml, sort_keys=False, default_flow_style=False)
                
    window.close()
            
with open('settings.yaml') as settings_yaml:
        settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)
        settings_yaml.close()
weekday = date.today().weekday()       
if weekday == 5 or weekday == 6:
    end_day_hour = int(settings[days[0] + '-hour'])
    end_day_minute = int(settings[days[0] + '-minute'])
else:
    end_day_hour = int(settings[days[weekday] + '-hour'])
    end_day_minute = int(settings[days[weekday] + '-minute'])
   
end_year_day = int(settings['last-day-day'])
end_year_month = int(settings['last-day-month'])    

while True:  # Event Loop
    event, values = window.read(timeout=1000)
    now = dt.now()
    
    end_of_school_year = dt(year=int(now.strftime('%Y')), month=end_year_month, day=end_year_day, hour=end_day_hour, minute=end_day_minute, second=0)
    end_of_day = dt(year=int(now.strftime('%Y')), month=int(now.strftime('%m')), day=int(now.strftime('%d')), hour=end_day_hour, minute=end_day_minute, second=0)
    
    if event == GUI.WIN_CLOSED:
        break
    if event == "settings-button":
        open_settings()
    window['DAYS-LEFT'].update(str(int(end_of_school_year.strftime('%j')) - int(now.strftime('%j'))))
    window['MINUTES-LEFT'].update(str(round((end_of_school_year - now).total_seconds() /60, 5)))
    window['SECONDS-LEFT'].update(str(int(round((end_of_school_year - now).total_seconds(), 0))))
    window['MINUTES-LEFT-TODAY'].update(str(round((end_of_day - now).total_seconds() /60, 5)))
    window['SECONDS-LEFT-TODAY'].update(str(int(round((end_of_day - now).total_seconds(), 0))))


window.close()