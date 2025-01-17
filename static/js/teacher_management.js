// Initialize DataTable
let teachersTable;

$(document).ready(function() {
    teachersTable = $('#teachersTable').DataTable({
        ajax: {
            url: '/get_teachers',
            dataSrc: ''
        },
        columns: [
            { data: 'name' },
            { data: 'email' },
            { data: 'department' },
            {
                data: null,
                render: function(data, type, row) {
                    return `
                        <div class="d-flex justify-content-around align-items-center">
                            <button class="btn btn-link p-0 me-2" onclick="viewTeacher(${row.id})">
                                <i class="bi bi-eye fs-5 text-info"></i>
                            </button>
                            <button class="btn btn-link p-0 me-2" onclick="editTeacher(${row.id})">
                                <i class="bi bi-pencil fs-5 text-warning"></i>
                            </button>
                            <button class="btn btn-link p-0" onclick="deleteTeacher(${row.id})">
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
function viewTeacher(id) {
    fetch(`/get_teachers/${id}`)
        .then(response => response.json())
        .then(teacher => {
            const modalContent = `
                <form>
                    <div class="mb-3">
                        <label class="form-label">Name</label>
                        <input type="text" class="form-control" value="${teacher.name}" readonly>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Department</label>
                        <input type="text" class="form-control" value="${teacher.department}" readonly>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" value="${teacher.email}" readonly>
                    </div>
                </form>
            `;
            
            $('#modalTitle').text('View Teacher Details');
            $('#modalContent').html(modalContent);
            new bootstrap.Modal(document.getElementById('actionModal')).show();
        })
        .catch(error => {
            toastr.error('Error fetching teacher details');
            console.error('Error:', error);
        });
}

// Edit Teacher
function editTeacher(id) {
    fetch(`/get_teachers/${id}`)
        .then(response => response.json())
        .then(teacher => {
            const modalContent = `
                <form id="editTeacherForm" onsubmit="updateTeacher(${id}); return false;">
                    <div class="mb-3">
                        <label class="form-label">Name</label>
                        <input type="text" class="form-control" name="name" value="${teacher.name}" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Department</label>
                        <select class="form-select" name="department" required>
                            <option ${teacher.department === 'Computer Science' ? 'selected' : ''}>Computer Science</option>
                            <option ${teacher.department === 'Mathematics' ? 'selected' : ''}>Mathematics</option>
                            <option ${teacher.department === 'Physics' ? 'selected' : ''}>Physics</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" name="email" value="${teacher.email}" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Update Teacher</button>
                </form>
            `;
            
            $('#modalTitle').text('Edit Teacher');
            $('#modalContent').html(modalContent);
            new bootstrap.Modal(document.getElementById('actionModal')).show();
        })
        .catch(error => {
            toastr.error('Error fetching teacher details');
            console.error('Error:', error);
        });
}

// Update Teacher
function updateTeacher(id) {
    const form = document.getElementById('editTeacherForm');
    const formData = new FormData(form);

    fetch(`/update_teacher/${id}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            toastr.success('Teacher updated successfully');
            teachersTable.ajax.reload();
            bootstrap.Modal.getInstance(document.getElementById('actionModal')).hide();
        } else {
            toastr.error(data.error || 'Error updating teacher');
        }
    })
    .catch(error => {
        toastr.error('Error updating teacher');
        console.error('Error:', error);
    });
}

// Delete Teacher
function deleteTeacher(id) {
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
            fetch(`/delete_teacher/${id}`, {
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
                    teachersTable.ajax.reload();
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
$(document).on('submit', 'form[action="/add_teacher"]', function(e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch('/add_teacher', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            toastr.success('Teacher added successfully');
            teachersTable.ajax.reload();
            bootstrap.Modal.getInstance(document.getElementById('actionModal')).hide();
        } else {
            toastr.error(data.error || 'Error adding teacher');
        }
    })
    .catch(error => {
        toastr.error('Error adding teacher');
        console.error('Error:', error);
    });
});




