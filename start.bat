@echo off
echo ============================================================
echo    PRATIK - Plateforme d'Accompagnement des Etudiants
echo ============================================================
echo.

REM Activer l'environnement virtuel
call .venv\Scripts\activate

echo [1/3] Verification de la base de donnees...
python manage.py migrate --noinput

echo.
echo [2/3] Collecte des fichiers statiques...
python manage.py collectstatic --noinput --clear

echo.
echo [3/3] Demarrage du serveur...
echo.
echo ============================================================
echo    Serveur demarre sur: http://localhost:8000
echo    Admin: http://localhost:8000/admin/
echo    API: http://localhost:8000/api/
echo ============================================================
echo.
echo Identifiants de test (mot de passe: user1234):
echo   - etudiant1@pratik.gf
echo   - ecole1@pratik.gf
echo   - entreprise1@pratik.gf
echo   - admin@pratik.gf (admin)
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo ============================================================
echo.

python manage.py runserver
