rmdir /S /Q C:\tmp\LunaTranslator
del C:\tmp\LunaTranslator.zip
xcopy C:\tmp\LunaTranslatorbuild\LunaTranslator_main.dist C:\tmp\LunaTranslator\LunaTranslator /e /y /I
xcopy C:\Users\11737\Documents\GitHub\LunaTranslator\fix C:\tmp\LunaTranslator /e /y /I
xcopy C:\Users\11737\Documents\GitHub\LunaTranslator\dependence C:\tmp\LunaTranslator\LunaTranslator /e /y /I
del C:\tmp\LunaTranslator\LunaTranslator\qt5qml.dll
del C:\tmp\LunaTranslator\LunaTranslator\qt5qmlmodels.dll
del C:\tmp\LunaTranslator\LunaTranslator\qt5quick.dll
rmdir /S /Q C:\tmp\LunaTranslator\LunaTranslator\translator\__pycache__
rmdir /S /Q C:\tmp\LunaTranslator\LunaTranslator\otherocr\__pycache__
rmdir /S /Q C:\tmp\LunaTranslator\LunaTranslator\postprocess\__pycache__

xcopy C:\tmp\LunaTranslator\ C:\dataH\LunaTranslator /e /y /I
pause