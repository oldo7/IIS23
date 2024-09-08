Úkolem zadání je vytvořit jednoduchý informační systém pro správu chytrých zařízení a vyhodnocování snímaných hodnot. Každé zařízení má nějaké unikátní označení, pomocí kterého ho uživatelé budou moci vhodně odlišit, typ (např. teploměr) a další atributy (např. popis, uživatelský alias apod.). Typ zařízení je reprezentován množinou parametrů. Každý parametr je definován názvem a množinou hodnot, kterých mohou zařízení nabývat (uvažujte pouze číselné hodnoty). Zařízení je možné shlukovat do skupin (tzv. systémů), přičemž každý systém má nějaký název, popis, svého správce a uživatele, kteří monitorují stavy zařízení daného systému. Správce definuje tzv. klíčové identifikátory výkonu (KPI), což jsou funkce jejichž vstupem je hodnota zvoleného parametru a výstupem logická hodnota: v pořádku/chyba (zvolte vhodnou množinu typů funkcí - např. teplota senzoru je/není větší než 20°C -> v pořádku/chyba apod.). Uživatelé pak monitorují, zda jsou pro dané KPI všechna zařízení v pořádku, případně některé z nich/všechny jsou ve stavu chyby. Uživatelé budou moci dále informační systém používat následujícím způsobem:

        administrátor
            spravuje uživatele
            má práva všech následujících rolí
        registrovaný uživatel
            zakládá systémy - stává se správcem systému
                registruje nová zařízení
                definuje KPI
                sdílí systém s jinými uživateli
            posílá žádosti o sdílení systému - po nasdílení se stává uživatelem systému
                monitoruje stavy zařízení a KPI
                prochází zařízení systému
        neregistrovaný uživatel
            prochází systémy - vidí základní metadata systému
        broker:
            uživatel, který bude moci aktualizovat hodnoty zařízení
            představuje simulaci aktualizace hodnot zařízení

    Náměty na rozšíření:

        napojení na reálný broker, který bude v periodicky obnovovat data z reálného zařízení - možný postup
        statistiky hodnot zařízení - možnost sledovat historická data zařízení a jejich vývoj ve formě grafů (zaměřte se mimo jiné na vhodné uložení dat)
        pokročilé vizualizace dat formou kvalitně navržených dashboardů
        pokročilé definice KPI
        rozumná architektura obnovy KPI s ohledem na velké množství zařízení a parametrů