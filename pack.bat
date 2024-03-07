@echo off

@REM 主目录的图片和记录和OCR模型和设置ini
set "source1=assets"
set "source2=log"
set "source3=models"
set "source4=settings.ini"

set "destination1=dist\main\_internal"

xcopy /s /i "%source1%" "%destination1%\%source1%"
xcopy /s /i "%source2%" "%destination1%\%source2%"
xcopy /s /i "%source3%" "%destination1%\%source3%"
copy /y "%source4%" "%destination1%"

@REM 工作区
set "source5=workbench\choices_dict.json"
set "source6=workbench\worklist.json"

set "destination2=dist\main\_internal\workbench\"

xcopy /s /i "%source5%" "%destination2%"
xcopy /s /i "%source6%" "%destination2%"

@REM OCR的一个警告dll
set "source7=onnxruntime_providers_shared.dll"
set "destination3=dist\main\_internal\onnxruntime\capi"

copy /y "%source7%" "%destination3%"

@REM OCR的依赖
if exist D:\anaconda (
    set "anaconda_folder=D:\anaconda"
) else (
    set "anaconda_folder=D:\Anaconda3"
)

set "source8=%anaconda_folder%\envs\py310\Lib\site-packages\rapidocr_onnxruntime\models"
set "source9=%anaconda_folder%\envs\py310\Lib\site-packages\rapidocr_onnxruntime\config.yaml"
set "destination4=dist\main\_internal\rapidocr_onnxruntime"

xcopy /s /i "%source8%" "%destination4%\models"
copy /y "%source9%" "%destination4%"

pause