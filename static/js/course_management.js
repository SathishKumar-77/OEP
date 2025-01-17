let studentsTable;

$(document).ready(function() {
    studentsTable = $('#studentsTable').DataTable({
        ajax: {
            url: '/get_students',
            dataSrc: ''
        },
        columns: [
            { data: 'name' },
            { data: 'email' },
            { data: 'gender' },
            {
                data: null,
                render: function(data, type, row) {
                    return `
                        <div class="d-flex justify-content-around align-items-center">
                            <button class="btn btn-link p-0 me-2" onclick="viewStudent(${row.id})">
                                <i class="bi bi-eye fs-5 text-info"></i>
                            </button>
                            <button class="btn btn-link p-0 me-2" onclick="editStudent(${row.id})">
                                <i class="bi bi-pencil fs-5 text-warning"></i>
                            </button>
                            <button class="btn btn-link p-0" onclick="deleteStudent(${row.id})">
                                <i class="bi bi-trash fs-5 text-danger"></i>
                            </button>
                        </div>
                    `;
                }
            }
        ],
        autoWidth: false, // Disable fixed widths
        responsive: true,
        dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>' +
             '<"row"<"col-sm-12"tr>>' +
             '<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Search teachers..."
        },
        order: [[0, 'asc']]
    });
});


// View Teacher Details
function viewStudent(id) {
    fetch(`/get_student/${id}`)
        .then(response => response.json())
        .then(student => {
            const modalContent = `
                <form>
                    <div class="mb-3">
                        <label class="form-label">Name</label>
                        <input type="text" class="form-control" value="${student.name}" readonly>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" value="${student.email}" readonly>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Gender</label>
                        <input type="text" class="form-control" value="${student.name}" readonly>
                    </div>
                        <div class="mb-3">
                        <label for="studentDob" class="form-label">Date of Birth</label>
                        <input name="dob" type="text" class="form-control" value="${student.dob}" required>
                    </div>
                </form>
            `;
            
            $('#modalTitle').text('View Teacher Details');
            $('#modalContent').html(modalContent);
            new bootstrap.Modal(document.getElementById('actionModal')).show();
        })
        .catch(error => {
            toastr.error('Error fetching student details');
            console.error('Error:', error);
        });
}

// Edit Teacher
function editStudent(id) {
    fetch(`/get_student/${id}`)
        .then(response => response.json())
        .then(student => {
            const modalContent = `
                <form id="editStudentForm" onsubmit="updateStudent(${id}); return false;">
                    <div class="mb-3">
                        <label class="form-label">Name</label>
                        <input type="text" class="form-control" name="name" value="${student.name}" required>
                    </div>
                        <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control"  name="email"  value="${student.email}" readonly>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Gender</label>
                        <input type="text" class="form-control" name="gender" value="${student.gender}" required>
                    </div>
                      </div>
                        <div class="mb-3">
                        <label class="form-label">Date of Birth</label>
                        <input name="dob" type="text" class="form-control" value="${student.dob}" required>
                    </div>
                     </div>
                        <div class="mb-3">
                        <label class="form-label">Department</label>
                        <input name="department" type="text" class="form-control" value="${student.department}" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Update Student</button>
                </form>
            `;
            
            $('#modalTitle').text('Edit Student');
            $('#modalContent').html(modalContent);
            new bootstrap.Modal(document.getElementById('actionModal')).show();
        })
        .catch(error => {
            toastr.error('Error fetching student details');
            console.error('Error:', error);
        });
}

// Update Teacher
function updateStudent(id) {
    const form = document.getElementById('editStudentForm');
    const formData = new FormData(form);

    fetch(`/update_student/${id}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            toastr.success('Student updated successfully');
            studentsTable.ajax.reload();
            bootstrap.Modal.getInstance(document.getElementById('actionModal')).hide();
        } else {
            toastr.error(data.error || 'Error updating student');
        }
    })
    .catch(error => {
        toastr.error('Error updating student');
        console.error('Error:', error);
    });
}

// Delete Teacher
function deleteStudent(id) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/delete_student/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    Swal.fire(
                        'Deleted!',
                        data.message,
                        'success'
                    );
                    studentsTable.ajax.reload();
                } else {
                    Swal.fire(
                        'Error!',
                        data.error || 'Error deleting teacher',
                        'error'
                    );
                }
            })
            .catch(error => {
                Swal.fire(
                    'Error!',
                    'Error deleting teacher',
                    'error'
                );
                console.error('Error:', error);
            });
        }
    });
}


// Handle Add Teacher Form Submit
$(document).on('submit', 'form[action="/add_student"]', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    console.log("Data:", formData);

    fetch('/add_student', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            toastr.success('Student added successfully');
            studentsTable.ajax.reload();
            bootstrap.Modal.getInstance(document.getElementById('actionModal')).hide();
        } else {
            toastr.error(data.error || 'Error adding student');
        }
    })
    .catch(error => {
        toastr.error('Error adding student');
        console.error('Error:', error);
    });
});



function handleCSVUpload(event) {
    const fileInput = event.target;
    const file = fileInput.files[0]; // Get the selected file

    if (!file) {
        alert("Please select a file.");
        return;
    }

    // Create FormData to send the file
    const formData = new FormData();
    formData.append('file', file);

    // Send the file to the backend using fetch
    fetch('/upload_students', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // alert(`Success: ${data.message}`);
            toastr.success(data.message);
            studentsTable.ajax.reload();
            if (data.errors.length > 0) {
                alert(`Errors:\n${data.errors.join('\n')}`);
            }
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error uploading file:', error);
        alert("An error occurred while uploading the file.");
    });
}
   function triggerUpload() {
        document.getElementById('csvUpload').click();
    }

    function handleCSVUpload(event) {
        // Show the loader
        document.getElementById('loader').style.display = 'flex';

        // Simulate processing delay for demonstration
        setTimeout(() => {
            alert('CSV file uploaded successfully!');
            // Hide the loader after the process
            document.getElementById('loader').style.display = 'none';
        }, 3000);
    }

    // Initialize DataTable
    $(document).ready(function () {
        $('#studentsTable').DataTable();
    });

    // Function to handle CSV upload with loader
    function triggerUpload() {
        document.getElementById('csvUpload').click();
    }

    function handleCSVUpload(event) {
        // Show the loader
        document.getElementById('loader').style.display = 'flex';

        // Simulate processing delay for demonstration
        setTimeout(() => {
            alert('CSV file uploaded successfully!');
            // Hide the loader after the process
            document.getElementById('loader').style.display = 'none';
        }, 3000);
    }

    // Initialize DataTable
    $(document).ready(function () {
        $('#studentsTable').DataTable();
    });




