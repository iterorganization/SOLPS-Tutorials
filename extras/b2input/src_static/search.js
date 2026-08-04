function initFuse(b2inputJSON) {
    // Flattening the hierarchical structure into an array of "switches"
    const switches = Object.keys(b2inputJSON).reduce(
        (list, modName) => list.concat(b2inputJSON[modName].categories.reduce(
        (list, cat) => list.concat(cat.groups.reduce(
            (list, group) => list.concat(group.switches.map(
            s => ({...s, group: group.name, category: cat.name, module: modName})
            )), []
        )), []
        )), []
    );
    return new Fuse(switches, {
        keys: ['name']
    });
}

function getLink(result) {
    return encodeURI(
        `${result.item.module}.html#${result.item.category}.${result.item.name}`
    );
}

function getUrlHashId() {
    return decodeURI(window.location.hash.substring(1));
}
