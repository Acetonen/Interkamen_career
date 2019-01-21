# Interkamen Program
### ver 1.16.0

![intro](readme_screenshots/intro.png)

This is corporative program of mining company to work with statistic and financial reports.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

For working with program source you need to install on your machine:
1. python 3.7+
And python frameworks:
1. pandas
2. matplotlib
3. openpyxl
4. Pillow
5. Sentry
6. bcrypt

### Installing

1. Copy repository or download files on your computer.
2. Unzip data.zip (test datafile) in root folder of program.
3. If you want to test login system launch interkamen.py
login: admin
password: admin
4. If you want to test program fast, launch dev_interkamen.py

## Built With

* [python3.6](https://www.python.org/) - Programming Language.
* [pandas](https://pandas.pydata.org/) - Python Data Analysis Library.
* [matplotlib](https://matplotlib.org/) - Python 2D plotting library.
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/#) - A Python library to read/write Excel 2010 xlsx/xlsm files.
* [Pillow](https://pillow.readthedocs.io/en/5.3.x/) - PIL is the Python Imaging Library.
* [Sentry](https://sentry.io/welcome/) - Open-source error tracking.
* [bcrypt](https://pypi.org/project/bcrypt/) - Good password hashing for your software and your servers.

## Contributing

Please email to acetonen@gmail.com for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning.
### what's new in 1.16.0:
MINOR:
1. Add sentry token input.
2. Add optional logger error configure.
3. Add argparser.
### what's new in 1.15.0:
MINOR:
1. Creation default admin account.
2. Add strong cryptography.
PATCH:
1. Fix logger bug with encoding log file.
2. Fix deleting workers.
3. Fix program version view.
4. Fix shift calendar.
### what's new in 1.14.0:
MINOR:
1. Merge backup module with email.
2. Add thread into status sender.
3. New non-brigade worker profession choosing from list.
4. Migrate users base for sample data.o
5. Add confirm_deletion_decorator in basic functions.
6. Add set_plotter_parametrs to standard functions.
7. Migrate all modules to __slots__.
PATCH:
1. Immediately working with main report after complete.
2. Add check_correcct_email into standard functions.
3. Add change user email.
### what's new in 1.13.1:
PATCH:
1. Fix 'loWWer' bug.
2. Fix problem with program path.
### what's new in 1.13.0:
MINOR:
1. Add threads to source file.
2. Add Autosum in drill passports.
3. Add event to show threads results.
4. Add thread to main report backup.
PATCH:
1. Tomorrow ITR list.
2. Fix corrupted log file.
3. Self destruction password check fix.
4. English literals in variant options.
5. Fix temp_drill_instrument_report bug.
### what's new in 1.12.0:
MINOR:
1. Add 'bcrypt' password hashing.
PATCH:
1. Fix showing brigade rating.
2. Add 'boss' to info type.
3. Add 0 option for float input.
4. Fix tomorrow color in career status html.
5. Add new drill passport name check.
6. Turn off logging system while using sentry.
7. Add expl works to career status automatically.
### what's new in 1.11.0:
MINOR:
1. Dump real brigade salary to exel.
2. Integrate sentry0.6.4 log system.
PATCH:
1. Fix bug with empty career status.
### what's new in 1.10.1:
MINOR:
1. Beautifully calendar of available days in mechanics report.
2. Count bits in rock in drill instrument report.
PATCH:
1. Fix dump to Exel path bug.
2. Fix unsave tamp drill instruments report.
### what's new in 1.10.0:
MINOR:
1. Add logging system.
2. Migrate from os.path to -> pathlib.
PATCH:
1. Change main script flow.
2. Fix career status if none works planed.
3. Add LOGGER to module scope in Users and Career Status.
4. Fix bug in mechanics report and reminder.
5. Add logger to all modules.
6. Add working with logs.
7. Add dump to exel for salary.
8. Automate count meters for drillers.
9. Round DSH in drill passports.
10. Add message to career status email.
11. Add exception to exit in main menu.
12. Add ready to input in career report.
13. Edit flow in All modules.
15. Delete ENTER for main menu.
### what's new in 1.9.0:
1. Add salary module.
2. Move career status to basic.
3. Add 'break' to news view
4. Add daily mechanic report in self menu.
5. Add recreation for daily report.
6. Add reminder to update career map.
7. Add edit workers profession in workers module.
8. Add different persents for brigadires.
9. Clean log file when enter program.
10. Add dump to exel for negabarites.
### what's new in 1.8.1:
1. Add Round to 0,5 in explosive.
2. Add totall in drill passports.
3. Add calendar in HTML career status.
4. Add non gabarites type of drill passport.
5. Normalise 5+ meters bareholes to 5 meters in exel drill passports.
6. Change volume count in exel drill passport.
7. Add except ConnectionResetError in email module.
### what's new in 1.8.0:
1. Create HTML dayli report to email send.
2. Change exl files destination.
3. Add dump ktu to exl in main report.
4. Fix adding temp drill report if rock mass not exist.
5. Add send html in email.
6. Add coordinates to working plans in daily report.
### what's new in 1.7.3:
1. Add total destruction for program data.
2. Add massive_type to drill pass parametrs.
### what's new in 1.7.2:
1. Create new package to work with exl files.
2. Remake AbsPath module.
3. Fix daily report bug.
### what's new in 1.7.1:
1. Fix news/ path bug.
2. Add exel dump for drill passport.
### what's new in 1.7.0:
1. Add news module.
2. Custom reminder.
3. Add stupid timer in master daily report.
### what's new in 1.6.1:
1. Make career status fill more user-friendly.
### what's new in 1.6.0:
1. Add career status module.
2. Add comma protect in all reports.
3. Add user with 'info' access.
### what's new in 1.5.1:
1. Add Working calendar module.
2. Add notifications for create mechanics and drill report.
### what's new in 1.5.0:
1. Add Drill passport.
2. Fix check date format.
### what's new in 1.4.1:
1. Fix date view in mechanics report.
2. Fix error when you try show rating and haven't brigades results yet.
### what's new in 1.4.0:
1. Add Brigade rating system.
2. Fix plots in report analysis module.
3. Move check_date_in_dataframe from mechanic_report to standart_functions.
4. Fix mechanic log.
5. Make standard date input.
6. Make submenus in admin meny by directions.
### what's new in 1.3.0:
1. Add maintenance calendar for mechanic.
2. Add reminder module.
3. Add reminder for maintenance.
4. Add 'stand reason' visualization to mechanics reports.
5. Fix bug in mechanics report when try to show stat and brigade 2 are empty.
6. Make backup after complete main report.
7. Merge stat_by_year and stat_by_month methods into stat_by_period.
### what's new in 1.2.0:
1. Add "edit report" in mechanics reports.
2. Remove 'exit by ENTER' from mechanics report.
3. Add correct check input hours in mechanics report.
4. Add more intuitive navigation in mechanic menu.
5. Add manual backup in administrator menu.
6. Replace txt backup log to pickle.
### what's new in 1.1.2:
1. Add availability to create drill report if main report not exist yet.
2. Fix backup bug.
### what's new in 1.1.1:
1. OOP style in pyplots.
2. Add "already exist" view for mechanics report.
3. Add brigadiers to salary list.
### what's new in 1.1.0:
1. Restructuring program files.
2. Add emailed module.
3. Add Email settings into administrator menu.
4. Add Mechanics report.
5. New administrator menus.
6. Make menu navigation simpler.
7. Add Email notifications for main report.
8. Add view reports by year in finance.
9. Add Employing date and penalties to workers.
### what's new in 1.0.1:
1. Remove 1,5 coefficient from buh. salary.
2. Add 'rock mass by month' plot in 'report_analysis'.
3. Colorful salary workers and drillers.

## Content and Instruction

### 1. Log in program
Content of program depend on user access. By default you have admin user access.
Admin user include in test data file.
To log in program:
Username: admin
Password: admin
### 2. Main menu
![main_menu](readme_screenshots/main_menu.png)

In header of main menu you may see different remainder that depend on user 'access'.

From this menu you have access to different sub-menus (depend on user access) and basic functions such are:

[7] - 'workers telephone numbers',
[8] - 'shifts calendar'
[9] - 'change password',
[10] - 'showing news'
[11] - 'career status'
[12] - 'exit program'.

Red menus are 'admin-only'

### 3. Admin menus
![admin_menu](readme_screenshots/admin_menu.png)

This menus give you access to:
1. read/delete/search in logs
2. create/delete/edit new user
3. create/show company structure
4. make/edit reminds for different users category
5. make backup of all data files
6. edit email notification and backup settings
7. add email to receive career status report
### 4. Workers menu
![workers_menu](readme_screenshots/workers_menu.png)

In this menu u can:
1. Create new worker
2. Show all workers from division
3. Show laying off workers (from worker archive)
4. Return worker from archive
5. Edit worker
6. Show anniversary workers
7. Create shift calendar of this year

### 5. Financial  menu
![finance_menu](readme_screenshots/finance.png)

In this menu u can:
1. Count workers salary
2. Create brigade rating total
3. Edit list of salary
4. Edit lists of brigadiers, salary workers, drillers

### 6. Mechanics menu
![mechanics_menu](readme_screenshots/mechanics_menu.png)

In this menu u can:
1. Show plots with all mechanics stats (KTI, KTG)
2. Create daily mechanic report, that goes to career status report automatically
3. Create report for machine maintenance
4. Edit report for machine maintenance
5. Working with maintenance calendar



### 5. Mining master menu
![statistic_menu](readme_screenshots/statistic.png)

In this menu u can:
1. Show all stats about brigade works, results, drill instruments
2. Create main master report that goes to main career report
3. Edit master report
4. Create drill passport
5. Edit drill passport
6. Create drill instrument report
7. Give rating to brigade
8. Create daily master report that goes to career status report

## Authors

* **Anton Kovalev** - *my gitHub* - [Acetonen](https://github.com/Acetonen/)

## License

This project is licensed under the GNU GPL v3.0  - see the [GNU](https://www.gnu.org/licenses/gpl-3.0.ru.html)

## Acknowledgments

* Thx [adw0rd](https://github.com/adw0rd) for great help.
