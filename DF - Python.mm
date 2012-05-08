<map version="0.9.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="DF - Python" ID="Freemind_Link_1868671804" CREATED="1273166469661" MODIFIED="1273166489192">
<hook NAME="MapStyle" max_node_width="600"/>
<node TEXT="Classes" POSITION="right" ID="Freemind_Link_1648294880" CREATED="1273166751201" MODIFIED="1273167202418" VSHIFT="7">
<node TEXT="GameMap" ID="Freemind_Link_1914625988" CREATED="1273166756856" MODIFIED="1273166761538">
<node TEXT="queued_moves" ID="Freemind_Link_1427776150" CREATED="1273167021526" MODIFIED="1273167024882">
<node TEXT="is a stack of moves for the dwarves to pick from, purely movement" ID="Freemind_Link_870808811" CREATED="1273167025871" MODIFIED="1273167040880"/>
</node>
<node TEXT="editqueue" ID="Freemind_Link_346480130" CREATED="1273167046627" MODIFIED="1273167078016">
<node TEXT="used for the array of various map designations" ID="Freemind_Link_1290703084" CREATED="1273167079192" MODIFIED="1273167091752"/>
</node>
</node>
<node TEXT="Mob" ID="Freemind_Link_1949236781" CREATED="1273166769507" MODIFIED="1273166773191">
<node TEXT="generic monster class, currently representing dwarves" ID="Freemind_Link_161757580" CREATED="1273166774960" MODIFIED="1273166782699"/>
<node TEXT="findPath()" ID="Freemind_Link_583848983" CREATED="1273166791152" MODIFIED="1273166804134">
<node TEXT="uses AStar.py&apos;s pathfinding based on the mobs .startpoint / .endpoint" ID="Freemind_Link_1860732708" CREATED="1273166805325" MODIFIED="1273166822035"/>
</node>
</node>
<node TEXT="Engine" ID="ID_1424473532" CREATED="1274646278285" MODIFIED="1274646281009"/>
<node TEXT="Item" ID="ID_786574552" CREATED="1274646284161" MODIFIED="1274646290996"/>
<node TEXT="MapTile" ID="ID_291260457" CREATED="1274646297273" MODIFIED="1274646301877"/>
<node TEXT="PriorityQueue" ID="ID_1808013664" CREATED="1274646305580" MODIFIED="1274646309404"/>
<node TEXT="PathFinder" ID="ID_222217780" CREATED="1274646311422" MODIFIED="1274646316806"/>
<node TEXT="Cursor" ID="ID_1744487136" CREATED="1274646320136" MODIFIED="1274646321541"/>
</node>
<node TEXT="Next Steps" POSITION="left" ID="Freemind_Link_1164217485" CREATED="1273167219867" MODIFIED="1273167225779">
<node TEXT="Classes" ID="Freemind_Link_1121435957" CREATED="1273167228765" MODIFIED="1273167230342">
<node TEXT="Job" ID="Freemind_Link_96401220" CREATED="1273167231752" MODIFIED="1273167272190">
<node TEXT="Dwarves that inherit from this particular class will be able to accept jobs from the various job types" ID="Freemind_Link_1578686790" CREATED="1273167236768" MODIFIED="1273167266472"/>
</node>
<node TEXT="Item" ID="Freemind_Link_1558174667" CREATED="1273167285861" MODIFIED="1273167288406">
<node TEXT="Basic item class for dwarves to interact with" ID="Freemind_Link_642527195" CREATED="1273167290752" MODIFIED="1273167299536"/>
<node TEXT="will include quality, build material information, and other statistics." ID="Freemind_Link_1286985973" CREATED="1273168382150" MODIFIED="1273168397424"/>
</node>
<node TEXT="Menu" ID="Freemind_Link_47597981" CREATED="1273167338575" MODIFIED="1273167341617">
<node TEXT="basic menu class will be needed to manage user input" ID="Freemind_Link_681462132" CREATED="1273167343339" MODIFIED="1273167352951"/>
</node>
<node TEXT="StatusUpdates" ID="Freemind_Link_344924531" CREATED="1273167361583" MODIFIED="1273167367170">
<node TEXT="special class to relay the most recent happening information" ID="Freemind_Link_510710923" CREATED="1273167368440" MODIFIED="1273167379128"/>
</node>
<node TEXT="Tile" ID="Freemind_Link_1983461906" CREATED="1273167426667" MODIFIED="1273167431318">
<node TEXT="Should contain extra info on what the tile contains, what type of material its made out of and and current floor, possibly stored hash or dictionary, should also include a state of being hidden or not aka viewable or visible flag.&#xa;&#xa;Water and Magma will be interesting and should be perhaps subclassed as tileContent" ID="Freemind_Link_1887125031" CREATED="1273167433117" MODIFIED="1273168198368"/>
</node>
<node TEXT="Material" ID="Freemind_Link_1579588830" CREATED="1273167490281" MODIFIED="1273167492186">
<node TEXT="basic material class that objects can inherit from different properties, can be set to have various k/v pairs, temperature, type, melting point, burning point..." ID="Freemind_Link_788223586" CREATED="1273167493237" MODIFIED="1273167620147"/>
</node>
<node TEXT="Mood" ID="Freemind_Link_538576224" CREATED="1273167718330" MODIFIED="1273167720032">
<node TEXT="basic mood class that critters can inherit from" ID="Freemind_Link_625566736" CREATED="1273167721676" MODIFIED="1273167728760"/>
</node>
<node TEXT="Possessions" ID="Freemind_Link_148387134" CREATED="1273167756300" MODIFIED="1273167759984">
<node TEXT="basic class to store the various items that a dwarf or critter has in its possession" ID="Freemind_Link_32476899" CREATED="1273167761253" MODIFIED="1273167776262"/>
</node>
<node TEXT="Room" ID="Freemind_Link_1696588278" CREATED="1273167787032" MODIFIED="1273167788953">
<node TEXT="basic room class that can be used to designate certain rooms" ID="Freemind_Link_1930498342" CREATED="1273167790316" MODIFIED="1273167802049"/>
</node>
<node TEXT="Zones" ID="Freemind_Link_1373376331" CREATED="1273167805175" MODIFIED="1273167808656">
<node TEXT="Similar to Rooms but for other designations" ID="Freemind_Link_1889663064" CREATED="1273167809925" MODIFIED="1273167822797"/>
</node>
<node TEXT="Mapgen" ID="Freemind_Link_69523021" CREATED="1273167860399" MODIFIED="1273167864488">
<node TEXT="placeholder for map generating classes, this can be its own section" ID="Freemind_Link_1896191211" CREATED="1273167865446" MODIFIED="1273167878396"/>
</node>
<node TEXT="WorldGen" ID="Freemind_Link_1242527021" CREATED="1273167882910" MODIFIED="1273167886625">
<node TEXT="placeholder for worldgen" ID="Freemind_Link_422163389" CREATED="1273167887410" MODIFIED="1273167897818"/>
</node>
<node TEXT="LoreGen" ID="Freemind_Link_1330408562" CREATED="1273167902940" MODIFIED="1273167906281">
<node TEXT="placeholder for lore generator" ID="Freemind_Link_567173257" CREATED="1273167907410" MODIFIED="1273167913496"/>
</node>
<node TEXT="Namegen" ID="Freemind_Link_1722521287" CREATED="1273167927198" MODIFIED="1273167930320">
<node TEXT="placeholder for name generator " ID="Freemind_Link_472770945" CREATED="1273167931512" MODIFIED="1273167937411"/>
</node>
<node TEXT="Stockpiles" ID="Freemind_Link_1723212258" CREATED="1273168099930" MODIFIED="1273168104144">
<node TEXT="like a room designation can be used to designate storage of certain item types." ID="Freemind_Link_186896910" CREATED="1273168105631" MODIFIED="1273168124260"/>
</node>
<node TEXT="Weapon" ID="Freemind_Link_98251878" CREATED="1273168212757" MODIFIED="1273168215411">
<node TEXT="This will be derived from the item class" ID="Freemind_Link_1269824414" CREATED="1273168232171" MODIFIED="1273168242656"/>
</node>
<node TEXT="Armor" ID="Freemind_Link_543725592" CREATED="1273168218349" MODIFIED="1273168220816">
<node TEXT="This will be derived from the item class" ID="Freemind_Link_652886412" CREATED="1273168232171" MODIFIED="1273168242656"/>
</node>
<node TEXT="Clothing" ID="Freemind_Link_1946484431" CREATED="1273168223022" MODIFIED="1273168224724">
<node TEXT="This will be derived from the item class" ID="Freemind_Link_143307533" CREATED="1273168232171" MODIFIED="1273168242656"/>
</node>
<node TEXT="GameState" ID="Freemind_Link_1946134178" CREATED="1273168276828" MODIFIED="1273168279184">
<node TEXT="will need to handle switching game modes from paused (edit mode) / to running state." ID="Freemind_Link_237166879" CREATED="1273168280001" MODIFIED="1273168298036"/>
</node>
<node TEXT="Description" ID="Freemind_Link_163717338" CREATED="1273168337120" MODIFIED="1273168344290">
<node TEXT="Will be either a sub class or class of its own attached to just about every object type." ID="Freemind_Link_1401386241" CREATED="1273168345357" MODIFIED="1273168363346"/>
</node>
<node TEXT="MapHandler" ID="Freemind_Link_1028673846" CREATED="1273168427665" MODIFIED="1273168438140">
<node TEXT="handle scrolling / moving the map around and manipulating it in various ways." ID="Freemind_Link_978756874" CREATED="1273168439534" MODIFIED="1273168453967"/>
</node>
<node TEXT="Building" ID="ID_102987062" CREATED="1273171021242" MODIFIED="1273171025316">
<node TEXT="Will be for building onto a tile, like a wall or chair or anything that can be built." ID="ID_1940659707" CREATED="1273171027427" MODIFIED="1273171094697">
<font NAME="SansSerif" SIZE="12" BOLD="false" ITALIC="false"/>
</node>
</node>
<node TEXT="InputHandler" ID="ID_759867371" CREATED="1273171121581" MODIFIED="1273171126388">
<node TEXT="will be used in conjunction with the gamestate and menu system for inputting commands." ID="ID_572127044" CREATED="1273171127829" MODIFIED="1273171141637"/>
</node>
</node>
</node>
<node TEXT="TODO" POSITION="right" ID="Freemind_Link_1275541596" CREATED="1273167956448" MODIFIED="1273167958463">
<node TEXT="Make screen resizable and have it modify the shown map size along with the menu remaining functional" ID="Freemind_Link_795503560" CREATED="1273167960075" MODIFIED="1273167976489"/>
<node TEXT="create viewport scrolling the map screen, only displaying part of the map" ID="Freemind_Link_1616658644" CREATED="1273167983468" MODIFIED="1273292090820"/>
</node>
<node TEXT="Files" POSITION="left" ID="ID_516734162" CREATED="1274646381538" MODIFIED="1274646383693">
<node TEXT="loader.py" ID="Freemind_Link_1550453063" CREATED="1273166536622" MODIFIED="1273166539791">
<node TEXT="used to load in pngs and create image / rect objects" ID="Freemind_Link_1312054250" CREATED="1273166832711" MODIFIED="1273166841746"/>
</node>
<node TEXT="gamemap.py" ID="_" CREATED="1273166499239" MODIFIED="1273166504402">
<node TEXT="mapdata" ID="Freemind_Link_1254317445" CREATED="1273166557394" MODIFIED="1273166563854">
<node TEXT="map data contains terrain type / movement cost" ID="Freemind_Link_1266015372" CREATED="1273166619981" MODIFIED="1273166632042"/>
</node>
<node TEXT="emapdata" ID="Freemind_Link_1322675258" CREATED="1273166567354" MODIFIED="1273166570352">
<node TEXT="editmode map with various designations, rendered after the map" ID="Freemind_Link_1466492630" CREATED="1273166572370" MODIFIED="1273166592480"/>
</node>
</node>
<node TEXT="cursor.py" ID="ID_884766556" CREATED="1274646395555" MODIFIED="1274646397491"/>
<node TEXT="engine.py" ID="ID_1557591136" CREATED="1274646399618" MODIFIED="1274646401664"/>
<node TEXT="item.py" ID="ID_1759126992" CREATED="1274646404712" MODIFIED="1274646406352"/>
<node TEXT="mob.py" ID="ID_1254168590" CREATED="1274646408978" MODIFIED="1274646410743"/>
<node TEXT="pathfinder.py" ID="ID_793649509" CREATED="1274646413214" MODIFIED="1274646415509"/>
<node TEXT="priorityqueue.py" ID="ID_351458301" CREATED="1274646417605" MODIFIED="1274646423777"/>
</node>
<node TEXT="Config Files" POSITION="right" ID="ID_781080495" CREATED="1274646435639" MODIFIED="1274646438168">
<node TEXT="cursor.cfg" ID="ID_893411595" CREATED="1274646440374" MODIFIED="1274646443059"/>
<node TEXT="gamemap.cfg" ID="ID_216898993" CREATED="1274646445186" MODIFIED="1274646448339"/>
<node TEXT="item.cfg" ID="ID_52243697" CREATED="1274646450545" MODIFIED="1274646452715"/>
<node TEXT="main.cfg" ID="ID_658518468" CREATED="1274646455467" MODIFIED="1274646458713"/>
<node TEXT="mob.cfg" ID="ID_1503396044" CREATED="1274646461449" MODIFIED="1274646464212"/>
</node>
</node>
</map>
