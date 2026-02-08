@echo off
REM Script pour exécuter les tests Pratik
REM Windows Batch Script

echo ========================================
echo   YANA PRATIK - TESTS AUTOMATISES
echo ========================================
echo.

REM Vérifier que l'environnement virtuel est activé
if not defined VIRTUAL_ENV (
    echo ERREUR: Environnement virtuel non active
    echo Executez: venv\Scripts\activate
    pause
    exit /b 1
)

echo Environnement virtuel: %VIRTUAL_ENV%
echo.

REM Menu de choix
echo Choisissez une option:
echo.
echo 1. Tous les tests
echo 2. Tests avec couverture
echo 3. Tests d'une app specifique
echo 4. Tests rapides (sans couverture)
echo 5. Rapport de couverture HTML
echo 6. Tests paralleles (rapide)
echo.

set /p choice="Votre choix (1-6): "

if "%choice%"=="1" (
    echo.
    echo Execution de tous les tests...
    pytest -v
) else if "%choice%"=="2" (
    echo.
    echo Execution des tests avec couverture...
    pytest --cov=apps --cov-report=html --cov-report=term-missing
    echo.
    echo Rapport HTML genere dans: htmlcov\index.html
) else if "%choice%"=="3" (
    echo.
    set /p app="Nom de l'app (users, internships, applications, etc.): "
    echo Execution des tests pour apps/%app%...
    pytest apps/%app%/tests.py -v
) else if "%choice%"=="4" (
    echo.
    echo Execution rapide des tests...
    pytest --tb=short
) else if "%choice%"=="5" (
    echo.
    echo Generation du rapport de couverture...
    pytest --cov=apps --cov-report=html
    echo.
    echo Ouverture du rapport...
    start htmlcov\index.html
) else if "%choice%"=="6" (
    echo.
    echo Execution des tests en parallele...
    pytest -n auto
) else (
    echo Choix invalide
    pause
    exit /b 1
)

echo.
echo ========================================
echo   TESTS TERMINES
echo ========================================
pause
