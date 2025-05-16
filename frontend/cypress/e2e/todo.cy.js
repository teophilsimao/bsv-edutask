describe('Logging into the system', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
  
    before(function () {
      // create a fabricated user from a fixture
      cy.fixture('user.json')
        .then((user) => {
          cy.request({
            method: 'POST',
            url: 'http://localhost:5001/users/create',
            form: true,
            body: user
          }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email

            const data = new URLSearchParams()
            data.append('title', 'Test Task')
            data.append('description', 'Test Task')
            data.append('userid', uid)
            data.append('url', 'testintesting')
            data.append('todos', ['Watch the vid boi'])

            cy.request({
                method: 'POST',
                url: 'http://localhost:5001/tasks/create',
                form: true,
                body: data.toString(),
            })
          })
        })
    })
  
    beforeEach(function () {
      cy.visit('http://localhost:3000')

      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)

      cy.get('form')
        .submit()
  
      cy.get('h1')
        .should('contain.text', 'Your tasks, ' + name)
    
      cy.get('img[src="http://i3.ytimg.com/vi/testintesting/hqdefault.jpg"]')
        .should('be.visible')
        .click()
      cy.get('h1')
        .should('contain.text', 'Test Task')
    })

    it('add task with valid input provided', () => {
        cy.get('input[placeholder="Add a new todo item"]')
          .type('Just chilling')

        cy.get('form.inline-form').submit()
        
        cy.get('li.todo-item')
          .should('contain.text', 'Just chilling')
    })

    it('add task without input', () => {
        cy.get('li.todo-item')
          .then($before => {
            const itemsBefore = $before.length

            cy.get('input[placeholder="Add a new todo item"]')
              .clear()
            cy.get('form.inline-form').submit()

            cy.get('li.todo-item')
              .should($after => {
                expect($after.length).to.eq(itemsBefore)
              })
          })
    })
  
    after(function () {
      // clean up by deleting the user from the database
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5001/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })
    })
  })