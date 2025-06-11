describe('Logging into the system', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
    let taskId
    let todoId
  
    before(function () {
      // create a fabricated user from a fixture
      cy.fixture('user.json')
        .then((user) => {
          cy.request({
            method: 'POST',
            url: 'http://localhost:5001/users/create',
            form: true,
            body: user
          }).then((res) => {
            uid = res.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email

            const data = new URLSearchParams()
            data.append('title', 'Test Task')
            data.append('description', 'Test Task')
            data.append('userid', uid)
            data.append('url', 'testintesting')
            data.append('todos', ['test todo'])

            return cy.request({
                method: 'POST',
                url: 'http://localhost:5001/tasks/create',
                form: true,
                body: data.toString(),
            }).then((res) => {
              taskId = res.body[0]._id.$oid
              cy.log(`Task ID: ${taskId}`);
              return cy.request(`http://localhost:5001/tasks/byid/${taskId}`)
            }).then((res) => {
              todoId = res.body.todos[0]._id.$oid
              cy.log(`Todo ID: ${todoId}`);
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

    it('add todo with valid input provided', () => {
        cy.get('input[placeholder="Add a new todo item"]')
          .type('Just chilling')

        cy.get('form.inline-form').submit()
        
        cy.get('.todo-item')
          .should('contain.text', 'Just chilling')
    })

    it('add todo without input', () => {
        cy.get('.todo-item')
          .then($before => {
            const itemsBefore = $before.length

            cy.get('input[placeholder="Add a new todo item"]')
              .clear()
            cy.get('form.inline-form').submit()

            cy.get('.todo-item')
              .should($after => {
                expect($after.length).to.eq(itemsBefore)
              })
          })
    })

    it('Mark active todo as done', () => {
      cy.request({
        method: 'PUT',
        url: `http://localhost:5001/todos/byid/${todoId}`,
        form: true,
        body: `data=${JSON.stringify({ "$set": { done: false } })}`,
      })

      cy.get('.todo-item').first().within(() => {
        cy.get('.checker').click();
        cy.get('.editable')
          .should('have.css', 'text-decoration')
          .and('include', 'line-through');
      });
    })

    it('Mark done todo as active', () => {
      cy.request({
        method: 'PUT',
        url: `http://localhost:5001/todos/byid/${todoId}`,
        form: true,
        body: `data=${JSON.stringify({ "$set": { done: true } })}`,
      })

      cy.get('.todo-item').first().within(() => {
        cy.get('.checker').click();
        cy.get('.editable')
          .should('have.css', 'text-decoration')
          .and('include', 'none');
      });
    })

    it('Delete todo', () => {
        cy.get('.todo-item')
            .then($before => {
              const itemsBefore = $before.length
              
              cy.get('.todo-item').first().within(() => {
                cy.get('.remover')
                  .click()
              })

            cy.get('.todo-item').should('have.length', itemsBefore - 1)
        })
    })

    // it('Delete a done todo', () => {
    //     cy.get('.todo-item')
    //         .then($before => {
    //             const itemsBefore = $before.length

    //             cy.get('.todo-item').first().within(() => {
    //                 cy.get('.checker')
    //                   .click()
    //                   .should('have.class', 'checked')
    //             })

    //             cy.get('.todo-item').first().within(() => {
    //                 cy.get('.remover')
    //                   .click()
    //             })

    //             cy.get('.todo-item').should('have.length', itemsBefore -1)
    //         })
    // })
  
    after(function () {
      // clean up by deleting the user from the database
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5001/users/${uid}`
      }).then((res) => {
        cy.log(res.body)
      })
    })
  })