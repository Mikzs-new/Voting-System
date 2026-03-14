const positions = new Map();

function add_position(){
    const positionInput = document.getElementById('position');
    const seatInput = document.getElementById('seat_count');

    const position = positionInput.value;
    const seat_count = seatInput.value;

    if(position === '' || seat_count === ''){
        return;
    }

    positions.set(position, seat_count);

    positionInput.value = '';
    seatInput.value = 1;
}

function create_election(){
    const positionsArray = Array.from(positions.entries());

    document.getElementById('positions').value = JSON.stringify(positionsArray);
}
