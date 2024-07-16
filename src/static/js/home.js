document.addEventListener("DOMContentLoaded", function () {
    let pathHistory = []; // Track the path history
    let currentContextMenu = null; // Track the current context menu

    const fetchAndRenderFileSystemStructure = (path = '') => {
        const endpoint = path ? `/files/file-system-structure/${user_id}/${encodeURIComponent(path)}` : `/files/file-system-structure/${user_id}`;
        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                const fileGrid = document.getElementById('fileGrid');
                fileGrid.innerHTML = ''; // Clear the file grid

                data.forEach(item => {
                    console.log(item);
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    fileItem.dataset.path = path ? `${path}/${item.name}` : item.name;

                    // Determine if the item is a file or a folder
                    if (item.permissions.startsWith('d')) {
                        fileItem.innerHTML = `<i class="fas fa-folder" style="color:#f39c12;"></i><span>${item.name}</span>`;
                    } else {
                        fileItem.innerHTML = `<i class="fas fa-file"></i><span>${item.name}</span>`;
                    }

                    fileItem.addEventListener('click', (e) => {
                        const newPath = e.currentTarget.dataset.path;
                        if (item.permissions.startsWith('d')) {
                            pathHistory.push(path); // Push the current path to history
                            fetchAndRenderFileSystemStructure(newPath);
                        } else {
                            alert(`File clicked: ${newPath}`);
                            // Add any additional actions for file click here
                        }
                    });

                    // Add context menu for file/folder options (e.g., delete)
                    fileItem.addEventListener('contextmenu', (e) => {
                        e.preventDefault();
                        hideCurrentContextMenu(); // Hide any existing context menu
                        showContextMenu(e.clientX, e.clientY, item.name, path);
                    });

                    fileGrid.appendChild(fileItem);
                });

                updateBreadcrumb(path);
                updateBackButton();
            })
            .catch(error => {
                console.error('Error fetching file system structure:', error);
            });
    };

    const showContextMenu = (x, y, fileName, path) => {
        const contextMenu = document.createElement('div');
        contextMenu.className = 'context-menu';
        contextMenu.style.position = 'fixed'; // Ensure it stays fixed on screen
        contextMenu.style.left = `${x}px`;
        contextMenu.style.top = `${y}px`;

        const deleteOption = document.createElement('div');
        deleteOption.className = 'context-menu-item';
        deleteOption.textContent = 'Delete';
        deleteOption.addEventListener('click', () => handleFileRemoval(fileName, path));

        const downloadOption = document.createElement('div');
        downloadOption.className = 'context-menu-item';
        downloadOption.textContent = 'Download';
        downloadOption.addEventListener('click', () => handleFileDownload(fileName, path));

        contextMenu.appendChild(deleteOption);
        contextMenu.appendChild(downloadOption);
        document.body.appendChild(contextMenu);
        currentContextMenu = contextMenu; // Track the current context menu

        // Remove context menu on any click outside
        document.addEventListener('click', hideCurrentContextMenu);
    };

    const hideCurrentContextMenu = () => {
        if (currentContextMenu) {
            currentContextMenu.remove();
            currentContextMenu = null;
            document.removeEventListener('click', hideCurrentContextMenu);
        }
    };

    const updateBreadcrumb = (path) => {
        const breadcrumbPath = document.getElementById('breadcrumbPath');
        breadcrumbPath.innerHTML = ''; // Clear the breadcrumb path
        const parts = path ? path.split('/') : [];

        parts.forEach((part, index) => {
            const breadcrumbPart = document.createElement('span');
            if (index === parts.length - 1) {
                breadcrumbPart.innerHTML = `<b>${part}</b>`;
            } else {
                breadcrumbPart.innerHTML = `<a href="#">${part}</a> / `;
                breadcrumbPart.addEventListener('click', () => {
                    const newPath = parts.slice(0, index + 1).join('/');
                    pathHistory.push(newPath); // Push the current path to history
                    fetchAndRenderFileSystemStructure(newPath);
                });
            }
            breadcrumbPath.appendChild(breadcrumbPart);
        });
    };

    const updateBackButton = () => {
        const backButton = document.getElementById('backButton');
        if (pathHistory.length > 0) {
            backButton.style.display = 'inline-block';
        } else {
            backButton.style.display = 'none';
        }
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (!file) {
            console.error('No file selected');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('/files/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                fetchAndRenderFileSystemStructure(); // Refresh file system after upload
            })
            .catch(error => {
                console.error('Error uploading file:', error);
            });
    };

    const handleFileRemoval = (fileName, path) => {
        if (!confirm(`Are you sure you want to delete ${fileName}?`)) {
            return;
        }

        const completePath = path ? `${path}/${fileName}` : fileName;

        fetch(`/files/remove/${user_id}/${encodeURIComponent(completePath)}`, {
            method: 'DELETE'
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                fetchAndRenderFileSystemStructure(path); // Refresh file system after removal
            })
            .catch(error => {
                console.error('Error removing file:', error);
            });
    };

    const handleFileDownload = (fileName, path) => {
        const completePath = path ? `${path}/${fileName}` : fileName;
        window.location.href = `/files/download/${user_id}/${encodeURIComponent(completePath)}`;
    };

    const fetchAndRenderStorageUsage = () => {
        fetch('/files/storage-usage')
            .then(response => response.json())
            .then(data => {
                const percentageUsed = data.percentage_used;
                const capacity = data.capacity;
                const used = data.used_storage;

                const storageUsed = document.getElementById('storageUsed');
                const storageInfoText = document.getElementById('storageInfoText');
                let usageColor = 'green';

                if (percentageUsed >= 80) {
                    usageColor = '#e74c3c';
                } else if (percentageUsed >= 60) {
                    usageColor = '#f39c12';
                }

                storageInfoText.textContent = `${used} out of ${capacity}`;
                storageUsed.style.width = `${percentageUsed}%`;
                storageUsed.style.backgroundColor = usageColor;

                const pieHTML = `<svg width="40" height="40" viewBox="0 0 40 40">
                                    <circle r="18" cx="20" cy="20" fill="transparent" stroke="#ecf0f1" stroke-width="4"/>
                                    <circle r="18" cx="20" cy="20" fill="transparent" stroke="${usageColor}" stroke-width="4"
                                    stroke-dasharray="${percentageUsed} ${100 - percentageUsed}" stroke-dashoffset="25"/>
                                    <text x="20" y="20" text-anchor="middle" dy=".3em" font-size="12" fill="#000">${percentageUsed}%</text>
                                </svg>`;

                document.getElementById('storagePie').innerHTML = pieHTML;
            })
            .catch(error => {
                console.error('Error fetching storage usage:', error);
            });
    };

    // Function to handle the browser back button
    window.addEventListener('popstate', function (event) {
        const state = event.state;
        if (state && state.path) {
            fetchAndRenderFileSystemStructure(state.path);
        } else {
            fetchAndRenderFileSystemStructure(); // Go back to the root if there's no state
        }
    });

    fetchAndRenderStorageUsage();
    fetchAndRenderFileSystemStructure();

    const toggleSidebarBtn = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    const storagePie = document.getElementById('storagePie');
    const storageBar = document.querySelector('.storage-bar');

    toggleSidebarBtn.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');

        const sidebarCollapsed = sidebar.classList.contains('collapsed');

        if (!sidebarCollapsed) {
            storagePie.classList.add('hidden');
            storageBar.classList.remove('hidden');
        } else {
            storagePie.classList.remove('hidden');
            storageBar.classList.add('hidden');
            fetchAndRenderStorageUsage();
        }
    });

    const backButton = document.getElementById('backButton');
    backButton.addEventListener('click', () => {
        const previousPath = pathHistory.pop(); // Get the previous path
        if (previousPath !== undefined) {
            // Add the current state to the browser history
            history.pushState({ path: previousPath }, '', '');
            fetchAndRenderFileSystemStructure(previousPath);
        } else {
            // Go back to the root if there's no previous path
            history.pushState({ path: '' }, '', '');
            fetchAndRenderFileSystemStructure();
        }
    });
});
