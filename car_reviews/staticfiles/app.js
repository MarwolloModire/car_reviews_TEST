document.addEventListener('DOMContentLoaded', () => {
	const loadDataButton = document.getElementById('load-data')
	const dataDiv = document.getElementById('data')

	loadDataButton.addEventListener('click', async () => {
		try {
			const response = await fetch('/api/cars/')
			const data = await response.json()
			dataDiv.innerHTML = JSON.stringify(data, null, 2)
		} catch (error) {
			console.error('Error fetching data:', error)
		}
	})
})
