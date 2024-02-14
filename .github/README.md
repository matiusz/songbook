# songbook

[![CircleCI](https://circleci.com/gh/matiusz/songbook/tree/hk-songbook.svg?style=svg)](https://circleci.com/gh/matiusz/songbook/tree/hk-songbook)

## songbook

Songbook is an easy to use tool for creating songbooks where each song is represented by a different file, allowing them to be easily shared or moved between different songbooks. It has its own display module or it can generate LaTeX files and compile them to pdf.

## Usage

### Without Docker
_Make sure to have installed everything needed from the [Requirements](#requirements) section_

#### Package Installation
You can install this application as a editable package with `pip install -e .`. This allows using `songbook` script from `cmd` 

#### GUI:
```cmd
python3 -m songbook.apps.run_gui
songbook run-gui          # if installed as package
```
Launches GUI application that allows editing and displaying songs.

#### Generate PDF:
```
python3 -m songbook.apps.create_pdf
songbook create_pdf       # if installed as package
```
Generates output PDF in root directory

#### Start Flask sever:
```
python3 -m songbook.apps.run_flask
songbook run-flask        # if installed as package
```
Starts a Flask server listening on address `0.0.0.0` with `PORT` envvar (default: `5000`)

#### Generate static site files:
```
python3 -m songbook.apps.freeze_flask
songbook freeze-flask     # if installed as package
```
Files are generated in `songbook/src/flask/build` directory

### With Docker
```
docker run -v $(pwd):/app --rm -it matiusz/songbook
```
and you can run the commands as above. Note that any command involving GUI may require additional setup, depending on the OS.

## Configuration

### Environment variables

`SONGBOOK_DATA_DIR` - directory in which songbook categories are located

`PORT` - port to start Flask server on


### Configuration file

The configuration can be altered by modifying the `config.json` file.

#### pdfSettings

*format* - e.g. a4paper, a5paper\
*sides* - oneside/twoside - if twoside is set pdf will have inner and outer margins and will include a blank page if chapter would start on an even page otherwise\
*margins* -
- *horizontal* - inner in case of twoside option, left otherwise
- *vertical* - top margin

*fontSize* - basic size of the font, supports sizes 10, 11, 12\
*lyricsFont, chordsFon*t - one of the fontcodes available e.g. here: https://www.overleaf.com/learn/latex/Font_typefaces#Reference_guide


## Requirements

- Python 3.8+ (builds are tested with 3.12)
- aiofiles

### Static deployment
- all modules listed in [requirements.txt](/requirements.txt)

### PDF compilation
- pdfTeX (suggested distribution - TeXLive)

### Full functionality
- pdfTeX
- [requirements_full.txt](/requirements_full.txt)
