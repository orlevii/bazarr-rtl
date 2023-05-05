# rtl-srt-fix

The pacakge for the `bazarr-rtl` CLI tool

## Usage
```bash
bazarr_rtl --help
```

### Known Bug
The following line is not fixed properly:
```
12 עונה 20: פרק

Expected:
עונה 20: פרק 12

Result:
עונה20 : פרק 12
```
