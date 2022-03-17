package main

import "fmt"

func main() {
	nums := []int{2, 3, 4}
	var sum int
	for _, num := range nums {
		sum += num
	}
	fmt.Println("sum: ", sum)

	str := "Hello world"
	for _, chr := range str {
		fmt.Printf("%c", chr)
	}
	fmt.Println()
}
