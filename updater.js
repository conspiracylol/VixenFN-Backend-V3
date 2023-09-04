const fs = require("fs");
const path = require("path");
const axios = require('axios');

async function updateAthena() {
    try {
        const defaultProfilesPath = path.join('./', 'profiles/default');
        const athenaProfileDefault = path.join('./', 'profiles/default', 'profile_athena.json');

        let athenaData;
        const req = await axios.get('https://fortnite-api.com/v2/cosmetics/br/');

        fs.readFile(athenaProfileDefault, async (err, _profileData) => {
            if (err) {
                console.log('[Profiles] Error when reading athena to update! Error: ' + err);
                return 'Error';
            }
            athenaData = await JSON.parse(_profileData);
            updateAthenaItems(athenaData, req.data.data);

            fs.writeFile(athenaProfileDefault, JSON.stringify(athenaData, null, 2), (errorlmfao) => {
                if (errorlmfao) {
                    console.log('[Profiles] failed to write profile!! Error: ' + errorlmfao);
                }
            });

            console.log('[Profiles] Reloaded cosmetics!');
        });
    } catch (error) {
        console.log('[Profiles] Failed to reload! Error in updateAthena()! Error: ' + error);
    }
}

function updateAthenaItems(athena, items) {
    items.forEach((cosmetic) => {
        const cosmeticVariants = [];
        if (cosmetic.variants) {
            cosmetic.variants.forEach((variant) => {
                const owned = variant.options.map((option) => option.tag);
                cosmeticVariants.push({
                    'channel': variant.channel,
                    'active': owned[0],
                    'owned': owned
                });
            });
        }

        athena.items[`${cosmetic.type.backendValue}:${cosmetic.id}`] = {
            'templateId': `${cosmetic.type.backendValue}:${cosmetic.id}`,
            'attributes': {
                'max_level_bonus': 69420,
                'level': 1,
                'item_seen': true,
                'rnd_sel_cnt': 0,
                'xp': 69420,
                'variants': cosmeticVariants,
                'favorite': false
            },
            'quantity': 1
        };
    });
}

function StartAutoUpdate() {
    
    // starts auto updater for cosmetics and shit!
    updateAthena();
    const halfHourInMilliseconds = 30 * 60 * 1000; // 30 minutes in milliseconds
    setInterval(updateAthena, halfHourInMilliseconds);

}
StartAutoUpdate();