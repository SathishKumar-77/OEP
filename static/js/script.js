// Modal and Interaction Management
function openModal(action) {
    const modalTitle = document.getElementById("modalTitle");
    const modalContent = document.getElementById("modalContent");

    switch (action) {
        case "addTeacher":
            modalTitle.textContent = "Add New Teacher";
            modalContent.innerHTML = `

            <form action="/add_teacher" method="POST">
    <div class="mb-3">
        <label class="form-label">Name</label>
        <input type="text" class="form-control" name="name" required>
    </div>
    <div class="mb-3">
        <label class="form-label">Department</label>
        <select class="form-select" name="department" required>
            <option>Computer Science</option>
            <option>Mathematics</option>
            <option>Physics</option>
        </select>
    </div>
    <div class="mb-3">
        <label for="teacherGender" class="form-label">Gender</label>
        <select class="form-select" id="teacherGender" name="gender" required>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
        </select>
    </div>
    <div class="mb-3">
        <label for="teacherEmail" class="form-label">Email ID</label>
        <input type="email" class="form-control" id="teacherEmail" name="email" required placeholder="Enter teacher's email">
    </div>
    <button type="submit" class="btn btn-primary">Add Teacher</button>
</form>


                        `;
            break;



        case "addStudent":
            modalTitle.textContent = "Add New Student";
            modalContent.innerHTML = `
                 <form action="/add_student" method="POST">
                    <div class="mb-3">
                        <label for="studentName" class="form-label">Full Name</label>
                        <input type="text" class="form-control" name="name" id="studentName" required placeholder="Enter student's full name">
                    </div>
                    <div class="mb-3">
        <label class="form-label">Department</label>
        <select class="form-select" name="department" required>
            <option>Computer Science</option>
            <option>Mathematics</option>
            <option>Physics</option>
        </select>
    </div>
                    <div class="mb-3">
                        <label for="studentRegNo" class="form-label">Registration Number</label>
                        <input type="text" name="reg_no" class="form-control" id="studentRegNo" required placeholder="Enter registration number">
                    </div>
                    <div class="mb-3">
                        <label for="studentDob" class="form-label">Date of Birth</label>
                        <input placeholder = "01/01/1999" name="dob" type="text" class="form-control" id="studentDob" required>
                    </div>
                    <div class="mb-3">
                        <label for="studentEmail" class="form-label">Email ID</label>
                        <input name="email" type="email" class="form-control" id="studentEmail" required placeholder="Enter student's email">
                    </div>
                    <div class="mb-3">
                        <label for="studentGender" class="form-label">Gender</label>
                        <select name="gender" class="form-select" id="studentGender" required>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Add Student</button>
                </form>
            `;
            case "addCourse":
            modalTitle.textContent = "Add New Course";
            modalContent.innerHTML = `
                 <form>
                    <div class="mb-3">
                        <label for="studentName" class="form-label">Course Name</label>
                        <input type="text" class="form-control" name="name" id="studentName" required placeholder="(Eg. M.Sc)">
                    </div>
                    <div class="mb-3">
        <label class="form-label">Department</label>
         <input type="text" class="form-control" name="department" id="departmentname" required placeholder="Department Name">
    </div>
             <div class="mb-3">
         <div class="input-group mb-3">
                <label class="form-label">Year</label>
                <input type="text" class="form-control" name="year[]" id="year" required placeholder="Year">
                <button type="button" class="btn btn-success" onclick="addYearField()">+</button>
            </div>   
                    <button type="submit" class="btn btn-primary">Add Student</button>
                </form>
            `;
            break;





        default:
            console.error("Unknown action: " + action);
            break;
    }

    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('actionModal'));
    modal.show();
}

    // Close the modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('actionModal'));
    modal.hide();
;
function toggleAnswer(answerId) {
    const answerElement = document.getElementById(answerId);
    if (answerElement.style.display === 'none') {
        answerElement.style.display = 'block';
    } else {
        answerElement.style.display = 'none';
    }
}



        function addYearField() {
            const container = document.getElementById('year-input-container');
            const newInputGroup = document.createElement('div');
            newInputGroup.classList.add('input-group', 'mb-3');

            // Create the new input field
            const newInput = document.createElement('input');
            newInput.type = 'text';
            newInput.classList.add('form-control');
            newInput.name = 'year[]';
            newInput.required = true;
            newInput.placeholder = 'Year';

            // Create the new remove button
            const removeButton = document.createElement('button');
            removeButton.type = 'button';
            removeButton.classList.add('btn', 'btn-danger');
            removeButton.innerText = '-';
            removeButton.onclick = () => newInputGroup.remove();

            // Append the input and button to the new input group
            newInputGroup.appendChild(newInput);
            newInputGroup.appendChild(removeButton);

            // Append the new input group to the container
            container.appendChild(newInputGroup);
        }
