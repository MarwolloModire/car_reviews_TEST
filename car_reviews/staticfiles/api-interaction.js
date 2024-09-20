document.addEventListener('DOMContentLoaded', function () {
	const loadDataButton = document.getElementById('loadDataButton')
	const dataContainer = document.getElementById('dataContainer')
	const addCarForm = document.getElementById('addCarForm')

	// Функция для загрузки данных
	const loadData = async () => {
		try {
			const token = localStorage.getItem('authToken')
			const response = await fetch('/api/cars/', {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json',
				},
			})

			if (response.ok) {
				const data = await response.json()
				dataContainer.innerHTML = '' // Очистка контейнера
				data.forEach(car => {
					const carElement = document.createElement('div')
					carElement.textContent = `Car Name: ${car.name}`
					dataContainer.appendChild(carElement)
				})
			} else {
				console.error('Ошибка загрузки данных', response.status)
			}
		} catch (error) {
			console.error('Ошибка:', error)
		}
	}

	// Обработчик клика по кнопке LOAD DATA
	loadDataButton.addEventListener('click', loadData)

	// Функция для добавления новой записи
	addCarForm.addEventListener('submit', async function (event) {
		event.preventDefault() // Отключаем стандартное поведение формы
		const carName = document.getElementById('carName').value

		try {
			const token = localStorage.getItem('authToken')
			const response = await fetch('/api/cars/', {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ name: carName }),
			})

			if (response.ok) {
				const newCar = await response.json()
				const carElement = document.createElement('div')
				carElement.textContent = `Car Name: ${newCar.name}`
				dataContainer.appendChild(carElement) // Добавляем новую запись на страницу
			} else {
				console.error('Ошибка при добавлении данных', response.status)
			}
		} catch (error) {
			console.error('Ошибка:', error)
		}
	})
})
