describe('Posts View', () => {
    it('displays posts list', () => {
      cy.visit('/posts')
      cy.get('.post-card').should('have.length.at.least', 1)
    })
  
    it('navigates to post detail', () => {
      cy.visit('/posts')
      cy.get('.post-card').first().click()
      cy.url().should('include', '/posts/')
    })
  })