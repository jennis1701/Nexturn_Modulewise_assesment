const expenseForm = document.getElementById('expenseForm');
const expenseTable = document.getElementById('expenseTable');
const summaryTable = document.getElementById('summaryTable');
let expenses = JSON.parse(localStorage.getItem('expenses')) || [];

function updateLocalStorage() {
    localStorage.setItem('expenses', JSON.stringify(expenses));
}

function renderExpenses() {
    expenseTable.innerHTML = '';
    expenses.forEach((expense, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>$${expense.amount}</td>
            <td>${expense.description}</td>
            <td><span class="category-badge category-${expense.category.toLowerCase()}">${expense.category}</span></td>
            <td><button class="btn btn-danger btn-sm" onclick="deleteExpense(${index})">Delete</button></td>
        `;
        expenseTable.appendChild(row);
    });
}

function renderSummary() {
    const summary = expenses.reduce((acc, expense) => {
        acc[expense.category] = (acc[expense.category] || 0) + expense.amount;
        return acc;
    }, {});

    summaryTable.innerHTML = '';
    for (const category in summary) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${category}</td>
            <td>$${summary[category]}</td>
        `;
        summaryTable.appendChild(row);
    }
}

function deleteExpense(index) {
    expenses.splice(index, 1);
    updateLocalStorage();
    renderExpenses();
    renderSummary();
}

expenseForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const amount = parseFloat(document.getElementById('amount').value);
    const description = document.getElementById('description').value;
    const category = document.getElementById('category').value;

    expenses.push({ amount, description, category });
    updateLocalStorage();
    renderExpenses();
    renderSummary();

    expenseForm.reset();
});

// Initial render
renderExpenses();
renderSummary();
