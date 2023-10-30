 ## FiveM Server Docker Container Generator

Célja ennek a projectnek hogy olyan dockerizált környezetet tudjunk készíteni amiben több FiveM szervert lehet futtatni. Tehát tudjunk "ugrálni" a szerverek között  relatív egyszerűen és tudjunk készíteni könnyedén újabb szervert.

 ## Szükséges programok
 - https://www.docker.com/products/docker-desktop/
 - Windowson belül kell tölteni a **pythont**-t (Microsoft Áruház)

**Fontos hogy mi után le töltöttük a repository utána adjuk ki ezt a parancsot a konzolban hogy a szükséges python package letöltésre kerüljenek amelyet a rendszer használ.**

**A parancs a következő:**

### `pip install -r requirements.txt` 

 ## Új szerver container létrehozása

 1. **create_server.bat** elindítása után adjunk meg egy szerver mappa nevet. (később ez lesz az adatbázis neve is).
 2. Elindul a txadmin telepítő, elnavigálunk a localhost:40120-ra és megadjuk a cmd ablakban megadott txAdmin azonosító kódot majd belépünk a txAdmin-ba.
 3. txAdmin-ba belépve a telepítő résznél válasszuk a ki a számunkra megfelelő templatett majd menjünk kattintsunk a next gombra.
 4. Következő oldalon adjuk meg a keymaster alapján a license kulcsunkat.
 5. Utána lesz egy Show/Hide gomb a license kulcs mező alatt erre kattintsunk rá.
 6. Lenyílik egy beállítási panel itt kell az adatbázis kapcsolodási adatokat megadni.
 7. Hostnál alapból localhost lesz ezt fontos átírni **mariadb**-re (különben nem fogunk tudni kapcsolodni az adatbázishoz)
 8. Ez után írjuk be username-hez hogy **user**
 9. Ez után írjuk be passwordnak hogy **root**
 10. Ez után adjuk meg az adatbázis nevét ez kizárólag az név lehet amit a szerver mappának adtunk az első lépésben. Tehát ide azt kell beírni amit megadtunk mint szerver mappa neve. Ezt látni fogod ott ahova másoltad az alap docker fájlokat lesz egy olyan nevű mappa amit megadtál. **Tehát a mappa nevét kell megadni csak akkor fog működni!**
 11. Ezek után csak next és végig megy a telepítő, várjuk meg még minden lebuildel első szerver indításkor.
 12. **CTRL+C** többszöri lenyomásával letudjuk állítani a containert, ha esetleg megkérdezi akkor Y és betudjuk zárni a cmd ablakot.


 ## Kész szerver container elindítása

 1. Indítsuk el a **run_server.bat**-ot és válasszuk ki a sorszámát az adott mappának amit indítani szeretnénk. 
 2. Be kell írnunk a sorszámot és entert kell nyomni hogy elinduljon a szerver container.
 3. Ezek után már lesz egy futó szerverünk amit localhost:40120-on elérünk és txAdmin minden funckióját tudjuk használni.

 ## Adatbázis elérés 

phpmyadmin elérés: **http://localhost:3333/**

Külső GUI-s adatbázis kezelő szoftver csatlakozáshoz szükséges adatok:
- Hosztnév/IP - **127.0.0.1**
- username - **user**
- password - **root**
- port - **3306**

Ha a fenti paramétereket megadtuk helyesen akkor feltudunk csatlakozni az adatbázisra külső szoftver segítségével.

## FiveM chat build probléma
Ha új szervert hozzunk létre és nem buildeli le elsőre a webpack a chat-et akkor a cache-t kell törölni majd 2-3x újraindítani a szervert és utána már jól lefogja buildelni a chatet. (Ez valószínűleg linux probléma a docker containerben)

## Új feature

Most már megadható hogy melyik artifact legyen használva minden új szerver készítésnél van rá opció ha üresen hagyjuk akkor latest verziót fogja használni a rendszer. 

Plusz bekerült a legutóbbi 10 verzió meg is jeleníti a konzol ami jelenleg elérhető mint artifact verzió. Így könnyítve a valid verziók keresését.


 ## Készítők
 Gellipapa és Csontvazharcos  
