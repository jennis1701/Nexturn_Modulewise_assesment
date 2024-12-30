//Bank Transaction System//
package main

import (
	"errors"
	"fmt"
)

// Account struct to hold account information
type Account struct {
	ID               int
	Name             string
	Balance          float64
	TransactionHistory []string
}

// Accounts slice to store all accounts
var accounts []Account

// Function to find an account by ID
func findAccountByID(id int) (*Account, error) {
	for i := range accounts {
		if accounts[i].ID == id {
			return &accounts[i], nil
		}
	}
	return nil, errors.New("Account not found")
}

// Deposit money into an account
func deposit(id int, amount float64) error {
	if amount <= 0 {
		return errors.New("Deposit amount must be greater than zero")
	}

	account, err := findAccountByID(id)
	if err != nil {
		return err
	}

	account.Balance += amount
	account.TransactionHistory = append(account.TransactionHistory, fmt.Sprintf("Deposited: %.2f", amount))
	return nil
}

// Withdraw money from an account
func withdraw(id int, amount float64) error {
	if amount <= 0 {
		return errors.New("Withdraw amount must be greater than zero")
	}

	account, err := findAccountByID(id)
	if err != nil {
		return err
	}

	if account.Balance < amount {
		return errors.New("Insufficient balance")
	}

	account.Balance -= amount
	account.TransactionHistory = append(account.TransactionHistory, fmt.Sprintf("Withdrew: %.2f", amount))
	return nil
}

// Display transaction history of an account
func displayTransactionHistory(id int) error {
	account, err := findAccountByID(id)
	if err != nil {
		return err
	}

	fmt.Printf("Transaction History for Account %d (%s):\n", account.ID, account.Name)
	for i, transaction := range account.TransactionHistory {
		fmt.Printf("%d. %s\n", i+1, transaction)
	}
	return nil
}

// Display the menu and handle user input
func menu() {
	for {
		fmt.Println("\nBank Transaction System")
		fmt.Println("1. Deposit")
		fmt.Println("2. Withdraw")
		fmt.Println("3. View Balance")
		fmt.Println("4. Transaction History")
		fmt.Println("5. Exit")
		fmt.Print("Choose an option: ")

		var choice int
		fmt.Scan(&choice)

		switch choice {
		case 1:
			var id int
			var amount float64
			fmt.Print("Enter Account ID: ")
			fmt.Scan(&id)
			fmt.Print("Enter Amount to Deposit: ")
			fmt.Scan(&amount)
			if err := deposit(id, amount); err != nil {
				fmt.Println("Error:", err)
			} else {
				fmt.Println("Deposit Successful.")
			}

		case 2:
			var id int
			var amount float64
			fmt.Print("Enter Account ID: ")
			fmt.Scan(&id)
			fmt.Print("Enter Amount to Withdraw: ")
			fmt.Scan(&amount)
			if err := withdraw(id, amount); err != nil {
				fmt.Println("Error:", err)
			} else {
				fmt.Println("Withdrawal Successful.")
			}

		case 3:
			var id int
			fmt.Print("Enter Account ID: ")
			fmt.Scan(&id)
			account, err := findAccountByID(id)
			if err != nil {
				fmt.Println("Error:", err)
			} else {
				fmt.Printf("Account Balance: %.2f\n", account.Balance)
			}

		case 4:
			var id int
			fmt.Print("Enter Account ID: ")
			fmt.Scan(&id)
			if err := displayTransactionHistory(id); err != nil {
				fmt.Println("Error:", err)
			}

		case 5:
			fmt.Println("Exiting system. Goodbye!")
			return

		default:
			fmt.Println("Invalid choice. Please try again.")
		}
	}
}

func main() {
	// Prepopulate some accounts
	accounts = []Account{
		{ID: 1, Name: "Priya", Balance: 5000},
		{ID: 2, Name: "Bobby", Balance: 3000},
		{ID: 3, Name: "Prakash", Balance: 10000},
	}

	menu()
}
