const positions = new Map();
const courses = new Set();
const levels = new Set();

function add_position(){
    const positionInput = document.getElementById('position');
    const seatInput = document.getElementById('seat_count');

    const position = positionInput.value.toLowerCase();
    const seat_count = seatInput.value;

    if(position === '' || seat_count === ''){
        return;
    }

    positions.set(position, seat_count);

    positionInput.value = '';
    seatInput.value = 1;
}

function add_level(){
    const levelInput = document.getElementById('year_level');
    
    levels.add(levelInput.value);
}

function add_all_level(){
    levels.add(1);
    levels.add(2);
    levels.add(3);
    levels.add(4);
}

function add_course(){
    const course = document.getElementById('course');

    courses.add(course.value)
}

function add_all_course(){
    const courseSelect = document.getElementById('course');
    const coursesArray = Array.from(courseSelect.options);
    coursesArray.forEach(course => {
        courses.add(parseInt(course.value));
    });
}

function create_election(){
    const positionsArray = Array.from(positions.entries());

    document.getElementById('positions').value = JSON.stringify(positionsArray);

    const yearLevelsArray = Array.from(levels);
    document.getElementById('year_levels').value = JSON.stringify(yearLevelsArray);

    const coursesArray = Array.from(courses);
    document.getElementById('courses').value = JSON.stringify(coursesArray);
    
}
