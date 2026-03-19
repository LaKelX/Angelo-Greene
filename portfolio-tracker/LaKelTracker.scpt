-- LaKel Portfolio Tracker
-- Save as Application, check "Stay open after run handler"

use AppleScript version "2.4"
use scripting additions

on run
    display notification "LaKel Portfolio Tracker Active" with title "LaKel"
    showMenu()
end run

on showMenu()
    set menuItems to {"━━━ HOLDINGS ━━━", "🟡 ASX - HOLD", "🟡 AMSC - HOLD", "─────────────", "━━━ BUY NOW ━━━", "🟢 LEU - Centrus Energy", "🟢 DDOG - Datadog", "🟢 CCJ - Cameco", "─────────────", "━━━ WATCHLIST ━━━", "🟡 VRT - WATCH", "🟡 AVAV - WATCH", "─────────────", "Refresh", "Quit"}

    set selectedItem to choose from list menuItems with title "LaKel Portfolio" with prompt "Portfolio Signals:" default items {"━━━ BUY NOW ━━━"}

    if selectedItem is not false then
        set choice to item 1 of selectedItem
        if choice is "Refresh" then
            showMenu()
        else if choice is "Quit" then
            quit
        else if choice contains "LEU" or choice contains "DDOG" or choice contains "CCJ" then
            display dialog choice & "

BUY SIGNAL ACTIVE" buttons {"OK"} default button "OK" with icon note
            showMenu()
        else
            showMenu()
        end if
    end if
end showMenu
