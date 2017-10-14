# -*- coding: utf-8 -*-

from gilded_rose import GildedRose
from item import Item


def test_normal_items():
    ''' Normal items should:
        - Decrease their quality by -1 until they reach sell_in date, then by -2
        - Quality >=0
    '''
    # Arrange
    test_cases = [
    # 1) Test element name and normal decrease
    (Item("cheddar",7,1),
     Item("cheddar",6,0)),
    # 2) Test boundary conditions
    # 2.1) Quality can not go below 0
    (Item("cheddar",0,0),
     Item("cheddar",-1,0)),
    # 2.2) What if something is already below its sell in date
    (Item("cheddar",-5,0),
     Item("cheddar",-6,0)),
    # 2.3) What if quality is already negative? Should be zero?
    # NOTE: No, this will not pass. Is not part of the specification to reset its value
    #(Item("cheddar",7,-3),
    # Item("cheddar",6,0)),
    # 2.4) If date passed, then should decrement by -2
    (Item("cheddar",-5,5),
     Item("cheddar",-6,3)),
    ]
    items = [test_case[0] for test_case in test_cases]
    gilded_rose = GildedRose(items)
    # Act
    gilded_rose.update_quality()
    # Assert
    for i,_ in enumerate(items):
       assert items[i].sell_in == test_cases[i][1].sell_in
       assert items[i].quality == test_cases[i][1].quality
       assert items[i].name == test_cases[i][1].name


def test_sulfuras_hand_of_ragnaros():
    ''' Sulfuras objects must be kept unchanged.
        - Its constant quality is 80
        - Its sell-in date should not be modified because it can't be sold
    '''
    test_cases = [
    # 1) Neither sell-in date nor quality should not change
    (Item("Sulfuras, Hand of Ragnaros",0,80),
     Item("Sulfuras, Hand of Ragnaros",0,80)),
    ]
    items = [test_case[0] for test_case in test_cases]
    gilded_rose = GildedRose(items)
    # Act
    gilded_rose.update_quality()
    # Assert
    for i,_ in enumerate(items):
       assert items[i].sell_in == test_cases[i][1].sell_in
       assert items[i].quality == test_cases[i][1].quality
       assert items[i].name == test_cases[i][1].name


def test_aged_brie():
    ''' Mmmm brie gets better with time
        - Its quality until sell-in date increases by 1
        - After its sell-in date, it increases by 2
    '''
    test_cases = [
    # 1) Check before its sell-in date
    (Item("Aged Brie",5,10),
     Item("Aged Brie",4,11)),
    # 2) Check after, extra mature Brie!
    (Item("Aged Brie",0,20),
     Item("Aged Brie",-1,22)),
    ]
    items = [test_case[0] for test_case in test_cases]
    gilded_rose = GildedRose(items)
    # Act
    gilded_rose.update_quality()
    # Assert
    for i,_ in enumerate(items):
       assert items[i].sell_in == test_cases[i][1].sell_in
       assert items[i].quality == test_cases[i][1].quality
       assert items[i].name == test_cases[i][1].name

def test_backstage_pass():
    """ Tickets to the concert increment price with time until date:
        - By +1 until 10 days before
        - By +2 between 10 and 5 days before
        - By +3 betwen 5 days and the same day of the concert
        - After the concert, the quality is zero
    """
    test_cases = [
    # 1) Check 27 days before
    (Item('Backstage passes to a TAFKAL80ETC concert', 27, 20),  
     Item('Backstage passes to a TAFKAL80ETC concert', 26, 21),),
    # 2) Check exactly 10 days before
    (Item('Backstage passes to a TAFKAL80ETC concert', 10, 20),  
     Item('Backstage passes to a TAFKAL80ETC concert', 9, 22),),
    # 3) Check 8 days before
    (Item('Backstage passes to a TAFKAL80ETC concert', 8, 20),  
     Item('Backstage passes to a TAFKAL80ETC concert', 7, 22),),
    # 4) Check exactly 5 days before
    (Item('Backstage passes to a TAFKAL80ETC concert', 5, 20),  
     Item('Backstage passes to a TAFKAL80ETC concert', 4, 23),),
    # 5) Check 3 days before
    (Item('Backstage passes to a TAFKAL80ETC concert', 3, 20),  
     Item('Backstage passes to a TAFKAL80ETC concert', 2, 23),),
    # 6) Check the day of the concert
    (Item('Backstage passes to a TAFKAL80ETC concert', 1, 20),     
     Item('Backstage passes to a TAFKAL80ETC concert', 0, 23),),
    # 7) Check 27 days after the concert
    (Item('Backstage passes to a TAFKAL80ETC concert', -27, 0),     
     Item('Backstage passes to a TAFKAL80ETC concert', -28, 0),),
    ]
    items = [test_case[0] for test_case in test_cases]
    gilded_rose = GildedRose(items)
    # Act
    gilded_rose.update_quality()
    # Assert
    for i,_ in enumerate(items):
       assert items[i].sell_in == test_cases[i][1].sell_in
       assert items[i].quality == test_cases[i][1].quality
       assert items[i].name == test_cases[i][1].name
