#Modèle 1 que l'on gardera après reflexion
'''
Orders= {- OrderDetails = {- orderNumber  
                           -quantityOrdered  
                           -priceEach  
                           -orderLineNumber
                           -Products = {-productCode  
                                        - productName  
                                        - productLine  
                                        - productScale  
                                        - productVendor  
                                        - productDescription  
                                        - quantityInShock 
                                        - buyPrice  
                                        - MSRP  
                                        }
                      }
         - orderDate 
         - requiredData
         - shippedData
         - status
         - comments
         - Customers = {- payments = {- customerNumber
                                      - checkNumber
                                      - paymentDate
                                      - amount
                                      }
                        - customerName  
                        - contactLastName  
                        - contactFirstName 
                        - phone  
                        - addressLine1  
                        - addressLine2  
                        - city  
                        - state  
                        - postalCode  
                        - country  
                        - salesRepEmployeeNumber  
                        - creditLimit 
                        }
         }

Employees = {- employeeNumber  
             - lastName 
             - firstName 
             - extension 
             - email  
             - Offices = {- OfficeCode  
                          - city  
                          - phone  
                          - adressLine1  
                          - adressLine2  
                          - state  
                          - country  
                          - postalCode 
                          - territory  
                        }  
             - reportsTo  
             - jobTitle 
             }
'''
'''------------------------------------------------------'''
#Modèle 2
'''
Orders = {- OrderDetails = {- orderNumber  
                            - quantityOrdered  
                            - priceEach  
                            - orderLineNumber
                            - Products = {-productCode  
                                          - productName  
                                          - productLine  
                                          - productScale  
                                          - productVendor  
                                          - productDescription  
                                          - quantityInShock 
                                          - buyPrice  
                                          - MSRP  
                                          }
                            }
          - orderDate 
          - requiredData
          - shippedData
          - status
          - comments
          - customerNumber
          }

Customers = {- payments = {- customerNumber
                           - checkNumber
                           - paymentDate
                           - amount
                           }
             - customerName  
             - contactLastName  
             - contactFirstName 
             - phone  
             - addressLine1  
             - addressLine2  
             - city  
             - state  
             - postalCode  
             - country  
             - salesRepEmployeeNumber  
             - creditLimit 
             }
}


Employees = {- employeeNumber  
             - lastName 
             - firstName 
             - extension 
             - email  
             - Offices = {- OfficeCode  
                          - city  
                          - phone  
                          - adressLine1  
                          - adressLine2  
                          - state  
                          - country  
                          - postalCode 
                          - territory  
                          }  
            - reportsTo  
            - jobTitle 
            }
'''
