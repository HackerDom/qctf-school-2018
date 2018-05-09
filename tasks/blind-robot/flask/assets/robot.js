var CUR_LEVEL = 0,
    CUR_X = 0,
    CUR_Y = 0;

var canvas = document.getElementById('myrobot'),
    context = canvas.getContext('2d');

var cell_size = 25;
canvas.width = cell_size * 3, 
canvas.height = cell_size * 3;

function write_error(text) {
    document.getElementById('error').innerHTML = text;
}

function resolve(level, x, y, callback) {
    var xhr = new XMLHttpRequest();
    var url = 'resolve/';
    var params = JSON.stringify({'level': level, 'x': x, 'y': y});
    xhr.open('POST', url, true);

    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState != XMLHttpRequest.DONE)
            return;

        if (xhr.status == 400)
            write_error(xhr.responseText);
        else
            callback(JSON.parse(xhr.responseText));
    }

    xhr.send(params);
}

function move(dx, dy) {
    write_error('');
    resolve(CUR_LEVEL, CUR_X + dx, CUR_Y + dy, function(info) {
        if (info.type != 'empty') {
            write_error('I can not go this direction!');
            return;
        }

        CUR_X += dx;
        CUR_Y += dy;

        draw(info.moves);
    });
}

function draw(moves) {
    context.fillStyle = '#555555';
    context.fillRect(0, 0, canvas.width, canvas.height);

    context.fillStyle = '#000000';
    context.fillRect(cell_size, cell_size, cell_size, cell_size);

    for (var move in moves) {
        offset = get_offset(move);
        if (moves[move])
            context.fillStyle = '#00EE00';
        else
            context.fillStyle = '#EE0000';

        context.fillRect(
            cell_size + offset.x * cell_size, 
            cell_size + offset.y * cell_size, 
            cell_size, 
            cell_size
        );
    }
}

function get_offset(direction) {
    return {
        'west':      {'x': -1, 'y':  0}, 
        'northwest': {'x': -1, 'y': -1}, 
        'north':     {'x':  0, 'y': -1}, 
        'northeast': {'x':  1, 'y': -1},
        'east':      {'x':  1, 'y':  0},
        'southeast': {'x':  1, 'y':  1},
        'south':     {'x':  0, 'y':  1},
        'southwest': {'x': -1, 'y':  1}
    }[direction];
}

function change_level(delta) {
    write_error('');
    resolve(CUR_LEVEL + delta, 0, 0, function(info) {
        CUR_LEVEL += delta;
        CUR_X = 0;
        CUR_Y = 0;

        draw(info.moves);
    });
}

window.onkeyup = function(e) {
    var key = e.keyCode ? e.keyCode : e.which;

    switch (key) {
        case 37:
            move(-1, 0);
            break;
        case 38:
            move(0, -1);
            break;
        case 39:
            move(1, 0);
            break;
        case 40:
            move(0, 1);
            break;       
    }
}

change_level(0);
